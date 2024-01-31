/**
 * A base implementation of the installments plugin. We recommend that custom logic be implemented
 * as a wrapper, or that it inherits and overrides this base implementation.
 */
require("../../utils/arrays.js");

const { DateCalc } = require("../../utils/DateCalc.js");
const { durationCalcMethod } = require("../../utils/utils.js");
const { PolicyContext } = require("../PolicyContext.js");
const { roundMoney, moneyUnit } = require('../../utils/common-options.js').options;

const global = globalThis;
const DE_MINIMUS_AMOUNT = 0.00000001;

const DEFAULT_OPTIONS = {
    // if true, will prevent installment start and end timestamps from overlapping
    preventStartAndEndTimestampOverlap: false,

    // Ensures at most one invoice covers the time before now
    collapsePastInstallments: true,

    // If true, places all fees on the first installment
    feesOnFirstInstallment: false,

    // Dictates where to place 'remainder' time when time span cannot be
    // evenly divided by requested intervals.
    // If true, placed at the front of the sequence; else, placed at the end
    remainderInstallmentsFirst: false,

    // Distributes any rounding differences across installments
    // If true, distributes to first installment;
    distributeCorrectionToFirstInstallment: false,
    // If true, distributes to last installment;
    distributeCorrectionToLastInstallment: false,
    //  else, distributes across all installments
    distributionRounding: null, // 'floor', 'ceil'
    distributionRoundingPrecision: 2, // 0 = dollar, 1 = dime, 2 = penny

    // if set, will ensure first installment has specific weight
    // in proportion to remaining installments
    firstInstallmentWeight: null,

    // if true, premium will be pulled from AuxData
    // and set to installmentPremiumWeight. installmentPremiumWeight should be an array of decimal values
    installmentPremiumFromAuxData: false,
    installmentPremiumWeight: undefined,

    // if true, fees will be pulled from AuxData. If true, it will overwrite the value of installmentFeeAmount set in options.
    installmentFeesFromAuxData: false,
    // nonzero amount will be applied to each installment, with given
    // fee name and description
    // installmentFeeAmount can be a decimal value or an array of decimal values
    installmentFeeAmount: 0,
    installmentFeeName: 'installment_fee', // this type must match definition in config
    installmentFeeDescription: 'Fee for payments over time',

    // non-commission charges summing to a value less than this amount
    // will result in plugin returning one single installment with all charges on it
    fullPayNowThreshold: 5,

    // if true, if the sum of non-commission charges is negative (a refund),
    // there will just be one installment with all charges placed on it
    alwaysFullPayCredit: true,

    // if true, a cancellation operation will result in the plugin returning a single
    // installment with all charges placed on it
    alwaysFullPayCancellation: false,

    // if 'upFront', will place all commission payments on the first installment; else,
    // will distribute commission charges like any other charge
    commissionPayments: 'onInvoice',

    // if absolute value of the total payable amount on a
    // given invoice is less than the carry-forward threshold, then that invoice's charges will be
    // moved to the next installment in the sequence
    carryForwardThreshold: 2,

    // specifies the acceptable difference in payable amounts across installments, which, if breached,
    // will result in logic to force evening by spread or writeOff (see levelingMethod)
    levelingThreshold: 1,

    // leveling method options:
    //  * 'spread': odd cents after leveling logic will distribute evenly over latter installments in a leveled segment
    //  * 'last': odd cents after leveling logic will be placed onto the last installment in a leveled segment
    //  * 'first': odd cents after leveling logic will be placed onto the first installment in a leveled segment
    //  * 'writeOff': odd cents will be accumulated onto a distinct written-off installment
    levelingMethod: 'spread',

    // if true, leveling will be performed on the series of installments across all terms; else,
    // leveling will be performed across installments within each term
    //  adjustAcrossTerms: true,

    // allows provision of explicit mapping between payment schedule names
    // and corresponding DateCalc `increment` values
    paymentScheduleToIncrement: {}, // supply if defaults insufficient

    // if provided, will use this value rather policy's default payment terms unit
    // possible values: 'year', 'month', 'day', 'hour', 'minute', 'second'
    defaultPaymentTermsUnit: undefined,

    // Day of month to consider as last day of month for preferred payment date
    preferredPaymentLastDayOfMonth: 31,
};

const DEFAULT_PAYMENT_SCHEDULE_TO_INCREMENT = {
    'upfront': 'eon',
    'annually': 'year',
    'monthly': 'month'
}

class InstallmentsGenerator {
    VERSION = '1.6';

    data;
    dateCalc;
    nowTimestamp;
    generatedInvoices;

    constructor(data, options = {}) {
        this.data = data;

        // Needed until SOCA-3655
        this.#normalizeChargeStarts();
        this.#destringifyInstallmentsData();

        this.dateCalc = new DateCalc(data.tenantTimeZone,
            parseInt(data.policy.originalContractStartTimestamp),
            'wholeDays');

        this.nowTimestamp = new Date().getTime(); // Timestamps are always UTC

        this.generatedInvoices = this.data.policy.invoices.map(inv => ({ startTimestamp: inv.startTimestamp, endTimestamp: inv.endTimestamp }));

        // Schedule names need to be declared in the config's policy.json
        let finalOptions = { ...{}, ...DEFAULT_OPTIONS, ...options };
        const paymentScheduleName = data.paymentScheduleName;

        // ensure payment schedule name has associated increment
        const paymentSchedules = { ...{}, ...DEFAULT_PAYMENT_SCHEDULE_TO_INCREMENT, ...finalOptions.paymentScheduleToIncrement };

        const incrementForSchedule = paymentSchedules[paymentScheduleName];

        if (incrementForSchedule === undefined) {
            throw new Error(`StartUIerror Plugin Error [Installment]: ${paymentScheduleName} not implemented! EndUIerror`);
        } else {
            finalOptions.increment = incrementForSchedule;
        }

        // Add logic for payment preferred date change. #JET-???
        // 1. Read overrides from Aux Data

        if (finalOptions.installmentPremiumFromAuxData || finalOptions.installmentFeesFromAuxData) {
            const auxDataSuffix = `${paymentScheduleName}_${this.#resolvePolicyTerm()?.replace('.', '-')}`;
            console.log('Aux Data Suffix: ', auxDataSuffix);

            if (finalOptions.installmentPremiumFromAuxData) {
                finalOptions = this.#addInstallmentOption(finalOptions, 'installmentPremiumWeight', `invoice_premiums_${auxDataSuffix}`);
            }

            if (finalOptions.installmentFeesFromAuxData) {
                finalOptions = this.#addInstallmentOption(finalOptions, 'installmentFeeAmount', `invoice_fees_${auxDataSuffix}`);
            }
        }

        // 2. Calculate preferred payment timestamp
        finalOptions.preferredPaymentTimestamp = this.#calcuatePreferredPaymentTimestamp(options, data);
        //

        console.log('Overrides from Aux Data: ', JSON.stringify({
            installmentPremiumWeightFromExternalRater: finalOptions.installmentPremiumWeight,
            installmentFeeAmountFromExternalRater: finalOptions.installmentFeeAmount === 0 ? undefined : finalOptions.installmentFeeAmount,
            preferredPaymentTimestamp: finalOptions.preferredPaymentTimestamp ? this.dateCalc.toMoment(finalOptions.preferredPaymentTimestamp).format('YYYY-MM-DD') : undefined,
        }));

        this.options = finalOptions;
    }

    #calcuatePreferredPaymentTimestamp(options, data) {
        const preferredPaymentTimestampString = global.debug ?
            options.preferredPaymentTimestamp : socotraApi.getAuxData(this.data?.policy?.locator, 'preferred_payment_date');
        const previousPreferredPaymentTimestampString = global.debug ?
            options.previousPreferredPaymentTimestamp : socotraApi.getAuxData(this.data?.policy?.locator, 'previous_preferred_payment_date');
        const policyStatus = global.debug ?
            options.policyStatus : socotraApi.getAuxData(this.data?.policy?.locator, 'policy_status');

        if (!preferredPaymentTimestampString) return undefined;
        if (
            data.transactionType === 'manual'
            && policyStatus.toLowerCase() === 'Cancellation Pending, Non-Payment of Premium'.toLowerCase()
            && preferredPaymentTimestampString !== previousPreferredPaymentTimestampString
        ) {
            throw new Error(`StartUIerror Plugin Error [Installment]: Preferred payment date cannot be changed when policy is in non-pay status. EndUIerror`);
        }

        console.log('Preferred Payment Dates from Aux Data', { current: preferredPaymentTimestampString, previous: previousPreferredPaymentTimestampString });
        let preferredPaymentTimestamp = preferredPaymentTimestampString ? parseInt(preferredPaymentTimestampString) : undefined;
        const lastGeneratedInvoiceEndTimestamp = Math.max(...this.generatedInvoices.map(inv => inv.endTimestamp));

        while (preferredPaymentTimestamp && preferredPaymentTimestamp < lastGeneratedInvoiceEndTimestamp) {
            preferredPaymentTimestamp = this.dateCalc.addToTimestamp(preferredPaymentTimestamp, 1, 'months');
        }
        console.log('Adjusted Preferred Payment Date', preferredPaymentTimestamp);

        return preferredPaymentTimestamp;
    }

    #addInstallmentOption(options, optionKey, auxDataKey) {
        const installmentItemFromExternalRater = global.debug ?
            options[optionKey] : socotraApi.getAuxData(this.data?.policy?.locator, auxDataKey);
        if (installmentItemFromExternalRater) {
            options = {
                ...options,
                [optionKey]: [],
            };
            installmentItemFromExternalRater.split(', ').forEach(
                item => options[optionKey].push(parseFloat(item))
            );
        }

        return options;
    }

    /**
     * Entry point: coordinates logic and returns valid installments series for the plugin
     * @returns {any[]}
     */
    getInstallments() {
        this.#markImmediateCharges();

        // We group by terms because invoicing is mostly scheduled one term at a time.
        // This creates terms with empty installments according to timing prefs.
        const terms = this.#createEmptyTermsAndInstallments();
        this.#calcInvoiceItems(terms);


        // Flatten the installments since we don't need to think about terms for remaining work
        let installments = terms.flatMap(t => t.installments);

        this.#setDueAndIssueDates(installments, true);

        // Ensure at most one invoice covers time before now
        if (this.options.collapsePastInstallments) {
            this.#collapseInstallmentsWithTimestampInPast(installments, this.nowTimestamp);
        }

        // Make sure nothing becomes due in the past: for past due dates make them due at
        // midnight tonight minus 1ms. Otherwise they will go into grace immediately.
        const midnightTonight = this.dateCalc.getEndOfDayTimestamp(this.nowTimestamp);
        for (const inst of installments.filter(inst => inst.dueTimestamp < midnightTonight))
            inst.dueTimestamp = midnightTonight;

        // For endorsements, already issued installment adjustments should have due timestamp as current
        if (['endorsement', 'cancellation', 'reinstatement', 'manual'].indexOf(this.data.operation) > -1) {
            for (const inst of installments.filter(inst => this.generatedInvoices.filter(
                inv => inst.startTimestamp >= inv.startTimestamp && inst.startTimestamp <= inv.endTimestamp
            ).length > 0))
                inst.issueTimestamp = inst.dueTimestamp = this.nowTimestamp;
        }

        //  if (this.options.adjustAcrossTerms) {
        //      installments = this.#carryForwardDeminimis(installments);
        //      installments = this.#levelInstallments(installments);
        //  }

        if (this.options.installmentFeeAmount && installments.length > 1)
            this.#applyInstallmentFees(installments, this.options.installmentFeeAmount);

        // Simplify and clean up the installments
        for (const inst of installments) {
            inst.invoiceItems = inst.invoiceItems.filter(ii => ii.amount !== 0);

            // Combine invoice items with the same chargeId
            this.#combineInvoiceItemsWithSameChargeId(inst);
        }

        this.#markEmptyInstallmentsForRemoval(installments, this.nowTimestamp);
        installments = installments.filter(inst => !inst.info.remove);

        // Delete unnecessary metadata
        for (const inst of installments) {
            delete inst.info;
            for (const ii of inst.invoiceItems)
                delete ii.type;
        }

        return { installments };
    }

    /**
     * Generates series to which charges will be assigned
     * @returns {*}
     */
    #createEmptyTermsAndInstallments() {
        const maxPolicyEnd = Math.max(this.data.policy.effectiveContractEndTimestamp,
            this.data.charges.max(ch => ch.coverageEndTimestamp),
            this.data.policy.modifications.max(m => m.effectiveTimestamp));

        let terms = this.data.policy
            .modifications
            .filter(mod => mod.name === 'modification.policy.create' || mod.name === 'modification.policy.renew')
            .map(mod => ({ startTimestamp: mod.effectiveTimestamp }))
            .filter(term => term.startTimestamp < maxPolicyEnd)
            .orderBy(term => term.startTimestamp);

        // Set the end timestamps
        for (let i = 0; i < terms.length; i++) {
            terms[i].endTimestamp = i < terms.length - 1 ? terms[i + 1].startTimestamp
                : maxPolicyEnd;
        }

        // Filter unused terms
        const earliestChargeTime = this.data.charges.min(ch => ch.coverageStartTimestamp);
        terms = terms.filter(term => term.endTimestamp > earliestChargeTime);

        // Put empty installments in each term
        for (let term of terms) {
            const span = this.dateCalc.getDateSequence(
                term.startTimestamp,
                term.endTimestamp,
                {
                    increment: this.options.increment,
                    // 2hour is for compressed config
                    anchorTimestamp: this.options.remainderInstallmentsFirst && ['month', '2hour', 'day'].indexOf(this.options.increment) > -1
                        ? term.endTimestamp : term.startTimestamp,
                    returnIntervals: true,
                    returnMetadata: true,
                    preferredBaseDayTimestamp: this.options.preferredPaymentTimestamp,
                    preferredLastDayOfMonth: this.options.preferredPaymentLastDayOfMonth,
                    preventStartAndEndTimestampOverlap: this.options.preventStartAndEndTimestampOverlap,
                });

            term.installments = span.sequence;

            for (let [i, inst] of term.installments.entries()) {
                inst.dueTimestamp = inst.startTimestamp;
                inst.invoiceItems = [];
                inst.installmentFees = [];
                inst.hasNonCommissionCharges = false;
                inst.writeOff = false;
                inst.feeWaived = false;
                inst.info = { installmentInTermNum: i };
            }

            if (span.sequence.length > 1) {
                const overlapAdjustment = this.options.preventStartAndEndTimestampOverlap ? 1 : 0;
                if (span.startCursor < term.startTimestamp) {
                    let firstInst = span.sequence[0];
                    firstInst.info.fraction = this.dateCalc.getDurationRatio(span.startCursor,
                        firstInst.startTimestamp, firstInst.endTimestamp + overlapAdjustment, true);
                }
                if (span.endCursor > term.endTimestamp) {
                    let lastInst = span.sequence.last();
                    lastInst.info.fraction = this.dateCalc.getDurationRatio(lastInst.startTimestamp,
                        lastInst.endTimestamp + overlapAdjustment, span.endCursor);
                }
                // Implemented for Jetty for monthly payment schedule
                span.sequence.filter(inst => span.fractionedItems.indexOf(inst.startTimestamp) > -1)?.forEach((inst, index) => {
                    inst.info.fraction = this.dateCalc.getDurationRatio(inst.startTimestamp,
                        inst.endTimestamp + overlapAdjustment, this.dateCalc.addToTimestamp(inst.startTimestamp, 1, 'months'));

                    if (index === 0) {
                        // Waive fee for the first installment if it is the preferred payment date
                        inst.feeWaived = inst.adjustedDueTimestamp = true;
                        inst.dueTimestamp = this.#calculatePreferredDueTimestamp(inst.dueTimestamp, span.baseDay);
                    }
                });
            }
        }

        return terms;
    }

    #calculatePreferredDueTimestamp(dueTimestamp, preferredBaseDay) {
        const preferredDueDate = this.dateCalc.toMoment(dueTimestamp);
        const currentBaseDay = preferredDueDate.date();
        this.dateCalc.incrementMomentByMonth(
            preferredDueDate,
            preferredBaseDay,
            preferredBaseDay > currentBaseDay ? -1 : 0
        );
        return preferredDueDate.valueOf() > Date.now() ? preferredDueDate.valueOf() : dueTimestamp;
    }

    /**
     * Assigns a given charge to one or more installments, in accordance with options
     * @param charge
     * @param installments
     */
    #placeChargeOnInstallments(charge, installments, lastChargeInTerm) {
        if (installments.length === 1 || charge.immediate) {
            if (charge.amount !== 0)
                installments[0].invoiceItems
                    .push({ chargeId: charge.chargeId, amount: charge.amount, type: charge.type });
            // } else if (installments.length === 1 || charge.immediate) {
            //     const amount = (
            //         charge.isNew === false
            //         && this.data.oldPaymentScheduleName?.toLowerCase() !== this.data.paymentScheduleName?.toLowerCase()
            //         && this.data.paymentScheduleName?.toLowerCase() === 'upfront'
            //     ) ? charge.originalAmount : charge.amount;
            //     if (amount !== 0)
            //         installments[0].invoiceItems
            //             .push({ chargeId: charge.chargeId, amount: amount, type: charge.type });
        } else {
            const weights = installments.map(inst => inst.info.fraction || 1);

            if (this.options.firstInstallmentWeight) {
                // ignores any fraction assigned to the first installment
                const subsequentWeight =
                    installments.sum(inst => inst.info.fraction || 1) - (installments[0].info.fraction || 1);

                weights[0] = this.options.firstInstallmentWeight * subsequentWeight /
                    (1 - this.options.firstInstallmentWeight);
            }

            /**
             * For each charge, identify which installments it
             * covers using its start and end dates. If it covers part of an installment,
             * weight that installment proportionally (for example, if a charge starts on
             * Jan 2 and ends Jan 29, it covers 27 days. For an installment that spans
             * all of January that charge would have weight 27/31, or about 0.871 for that
             * installment.)
             */
            for (let i = 0; i < installments.length; i++) {
                let inst = installments[i];
                if (charge.coverageStartTimestamp >= inst.endTimestamp
                    || charge.coverageEndTimestamp <= inst.startTimestamp) {
                    weights[i] = 0;
                }

                else if (charge.coverageStartTimestamp > inst.startTimestamp
                    || charge.coverageEndTimestamp < inst.endTimestamp) {

                    /**
                     * Determine proportional weight (num = numerator, den = denominator),
                     * basically saying "this charge fits in this installment, but how much of it
                     * actually fits in this installment?"
                     */
                    const num = this.dateCalc.getDuration(Math.max(inst.startTimestamp, charge.coverageStartTimestamp),
                        Math.min(inst.endTimestamp, charge.coverageEndTimestamp));
                    const den = this.dateCalc.getDuration(inst.startTimestamp,
                        inst.endTimestamp);
                    if (num <= 0) {
                        weights[i] = 0;
                    }
                    else if (den > num) {
                        weights[i] *= num / den;
                    }
                }
            }

            let distribution;
            if (charge.originalAmount === 0 || this.#isRefundFromOvercharge(charge)) {
                distribution = weights.map(w => 0);
                distribution[0] = charge.amount;
            }

            else if (charge.previouslyInvoicedAmount) {
                /**
                 * Reduce the installment amounts by the previously billed amounts
                 * We do this instead of starting with the charge.amount (which is the net amount)
                 * because doing that would allocate amounts to the previously billed time spans
                 * and cause distortion (essentially billing too early.)
                 */
                const isNeg = charge.originalAmount < 0;

                distribution = this.#distributeAmountWeighted(Math.abs(charge.originalAmount), weights, lastChargeInTerm);
                let prevAmt = isNeg ? -charge.previouslyInvoicedAmount : charge.previouslyInvoicedAmount;

                // Subtract from the installments starting with the earliest in the term to
                // reduce the charge original amount to the amount net of previous invoices
                for (let i = 0; i < distribution.length; i++) {
                    if (prevAmt < 0) {
                        distribution[i] -= prevAmt;
                        break;
                    }

                    else if (prevAmt === 0) {
                        break;
                    } else {
                        const amt = Math.min(prevAmt, distribution[i]);
                        distribution[i] -= amt;
                        prevAmt -= amt;
                    }
                }

                if (isNeg) {
                    distribution = distribution.map(d => -d);
                }

            } else {
                distribution = this.#distributeAmountWeighted(charge.amount, weights, lastChargeInTerm);
            }

            // for (let i = 0; i < installments.length; i++) {
            for (let [i, installment] of installments.entries()) {
                const correspondingDistributionAmount = distribution[i];
                if (Math.abs(correspondingDistributionAmount) > DE_MINIMUS_AMOUNT) {
                    installment.invoiceItems.push(
                        { chargeId: charge.chargeId, amount: correspondingDistributionAmount, type: charge.type });
                }
            }
        }
    }

    /**
     * Updates baseTimestamp according to offsetDays and adjustToMidnight
     * @param baseTimestamp
     * @param offsetAmount
     * @param adjustToMidnight
     * @param offsetUnit
     * @returns {*}
     */
    #getTimestampWithOffset(baseTimestamp, offsetAmount, adjustToMidnight, offsetUnit = 'days') {
        if (offsetAmount) {
            baseTimestamp = this.dateCalc.addToTimestamp(baseTimestamp,
                offsetAmount,
                offsetUnit);
        }

        if (adjustToMidnight) {
            baseTimestamp = this.dateCalc.getEndOfDayTimestamp(baseTimestamp);
        }

        return baseTimestamp;
    }


    /**
     * Applies any applicable fees to the installments series
     * @param installments
     * @param amount
     */
    #applyInstallmentFees(installments, amount) {
        if (!amount) return;

        // Installment fees go on non-zero invoices, including the first in the term
        installments.filter(
            inst => this.#getPayableAmountForInstallment(inst) > DE_MINIMUS_AMOUNT
                && !inst.writeOff
                && !inst.feeWaived
                && inst.info.installmentInTermNum >= 0
                && this.generatedInvoices.filter(inv =>
                    inst.startTimestamp >= inv.startTimestamp
                    && inst.startTimestamp < inv.endTimestamp
                ).length === 0
        ).forEach((inst, index) => {
            if (inst.feeWaived) {
                amount.splice(index, 0, 0);
                return;
            }
            const feeAmount = Array.isArray(amount) && index >= amount.length ? amount[0] : amount[index];
            inst.installmentFees.push({
                feeName: this.options.installmentFeeName,
                description: this.options.installmentFeeDescription,
                amount: feeAmount,
            });
        });

    }

    /**
     * Sets due and issue dates for installments set
     * @param installments
     * @param dueAtMidnight
     */
    #setDueAndIssueDates(installments, dueAtMidnight = true) {

        // Later we adjust to make sure invoices aren't due in the past
        // So don't worry about that that now.
        for (const inst of installments) {
            const installmentDueTimestamp = inst.adjustedDueTimestamp ? inst.dueTimestamp : inst.startTimestamp;
            inst.issueTimestamp = this.#getTimestampWithOffset(
                installmentDueTimestamp,
                -this.data.defaultPaymentTerms.amount,
                false,
                this.options.defaultPaymentTermsUnit
            );
            inst.dueTimestamp = dueAtMidnight ? this.dateCalc.getEndOfDayTimestamp(installmentDueTimestamp)
                : installmentDueTimestamp;
        }
    }


    /**
     * Make sure at most one installment is in the past; we don't want to immediately
     * send multiple invoices.
     *
     * Note: This can mutate the input array.
     *
     * Defaults using startTimestamp as the comparison.
     * To compare with issue timestamp, e.g., pass (inst => inst.issueTimestamp)
     * for dateRefFn
     * @param installments
     * @param nowTimestamp
     * @param dateRefFn
     */
    #collapseInstallmentsWithTimestampInPast(installments, nowTimestamp, dateRefFn = inst => inst.startTimestamp) {
        const pastInstallments = installments.filter(inst => dateRefFn(inst) <= nowTimestamp);
        if (pastInstallments.length > 1) {
            // Move all past invoice items to the last past installment
            const pastItems = pastInstallments.flatMap(inst => inst.invoiceItems);
            for (let i = 0; i < pastInstallments.length - 1; i++)
                pastInstallments[i].invoiceItems = [];
            pastInstallments.last().invoiceItems = pastItems;
        }
    }

    /**
     * Distributes the amount across a number of segments using the provided
     * weights, with each segment being rounded to two decimal places. If the
     * amount does not divide evenly then segment amounts could differ by +/ 0.01.
     * @param amount
     * @param weights
     * @returns {*}
     */
    #distributeAmountWeighted(amount, weights, lastChargeInTerm) {

        // Refactor weights if received from external rater
        if (this.options.installmentPremiumFromAuxData && this.options.installmentPremiumWeight) {
            if (amount > 0 && this.options.installmentPremiumWeight.sum() === 0) {
                throw new Error(`StartUIerror Plugin Error [Installment]: All distribution weights ${JSON.stringify(this.options.installmentPremiumWeight)} cannot be zero with a positive amount. EndUIerror`);
            }

            weights.forEach((weight, index) => {
                if (index < this.options.installmentPremiumWeight.length) {
                    weights[index] = weight * (this.options.installmentPremiumWeight[index] ?? 1);
                }
            });
        }

        const totalWeight = weights.sum();

        if (Math.abs(totalWeight) < DE_MINIMUS_AMOUNT) {
            return this.#distributeAmountWeighted(amount, weights.map(w => 1), lastChargeInTerm);
        }

        const dist = [];
        for (let i = 0; i < weights.length; i++) {
            let distAmount = roundMoney(amount * weights[i] / totalWeight);
            const distributionRounding = this.options.distributionRounding;
            const distributionRoundingDecimal = this.options.distributionRoundingPrecision;
            if (distributionRounding && distributionRoundingDecimal) {
                distAmount = Math[distributionRounding](distAmount * Math.pow(10, distributionRoundingDecimal)) / Math.pow(10, distributionRoundingDecimal);
            }

            // Handle <$1 invoices
            if (lastChargeInTerm && this.installments[i] + distAmount < 1) {
                distAmount += 1;
            }
            dist.push(distAmount);
        }

        const finalDist = this.#correctDistributionRounding(amount, dist);
        for (let i = 0; i < finalDist.length; i++) {
            this.installments[i] += finalDist[i];
        }
        return finalDist;
    }

    /**
     * Evenly distributes any shortfalls detected due to rounding
     * @param amount
     * @param distribution
     * @returns {*}
     */
    #correctDistributionRounding(amount, distribution) {
        let unitShortfall = Math.round((amount - distribution.sum()) / moneyUnit);
        if (unitShortfall) {
            let correction = unitShortfall >= 0 ? moneyUnit : -moneyUnit;
            unitShortfall = Math.abs(unitShortfall);

            if (this.options.distributeCorrectionToFirstInstallment) {
                let i = 0;
                for (i = 0; i < distribution.length; i++) {
                    if (Math.abs(distribution[i]) > 0) break;
                }
                distribution[i] = roundMoney(distribution[i] + correction * unitShortfall);
            } else if (this.options.distributeCorrectionToLastInstallment) {
                distribution[distribution.length - 1] = roundMoney(distribution[distribution.length - 1] + correction * unitShortfall);
            } else {
                let cursor = 0;
                while (unitShortfall) {
                    let idx = cursor++ % distribution.length;

                    // protect specific weighting val on first installment
                    if (idx === 0 && this.options.firstInstallmentWeight != null) {
                        continue;
                    }

                    if (distribution[idx] !== 0 || cursor > 1000) {
                        unitShortfall--;
                        distribution[idx] = roundMoney(distribution[idx] + correction);
                    }
                }
            }

            if (roundMoney(distribution.sum()) !== roundMoney(amount)) {
                throw new Error(`StartUIerror Plugin Error [Installment]: distributing ${amount} sums to ${distribution.sum()} EndUIerror`);
            }
        }

        return distribution;
    }

    /**
     * Returns sum of payable amounts for an installment
     * @param installment
     * @returns {*}
     */
    #getPayableAmountForInstallment(installment) {
        return installment.invoiceItems.sum(ii => ii.type === 'commission' ? 0 : ii.amount);
    }

    /**
     * The coverageStartTimestamp of charges is adjusted to exclude previously invoiced
     * amounts. This changes the charges to cover the entire period, which prevents
     * timing distortions on endorsements.
     *
     * We should probably change this in the platform, but it will require a feature
     * flag. See SOCA-3655.
     */
    #normalizeChargeStarts() {
        const pc = new PolicyContext(this.data.policy);
        for (const ch of this.data.charges) {
            if (ch.perilCharacteristicsLocator) {
                const chars = pc.getPerilCharacteristics(ch.perilCharacteristicsLocator);
                if (chars) {
                    ch.coverageStartTimestamp = chars.coverageStartTimestamp;
                    ch.coverageEndTimestamp = chars.coverageEndTimestamp;
                }
            } else {
                // no peril characteristics locator suggests this is a fee
                const fee = this.data.policy.fees.find(f => f.locator === ch.feeLocator);
                if (fee) {
                    ch.coverageStartTimestamp = fee.startTimestamp;
                    ch.coverageEndTimestamp = fee.endTimestamp;
                }
            }
        }
    }

    #resolvePolicyTerm() {
        const pc = new PolicyContext(this.data.policy);
        const chars = pc.allCharacteristics();
        // TODO: Change to getFieldValueFloat once resolved from Coherent rater
        const policyTerm = pc.getFieldValue(chars[chars?.length - 1], 'policy_term');

        return policyTerm;
    }

    /**
     * Determine whether some charge appears to represent an "overcharge" scenario
     * @param charge
     * @returns {boolean}
     */
    #isRefundFromOvercharge(charge) {
        return charge.amount < 0 &&
            charge.previouslyInvoicedAmount > charge.originalAmount &&
            charge.previouslyInvoicedAmount > 0 &&
            charge.originalAmount > 0;
    }

    /**
     * Determine whether conditions suggest all charges should go on a single installment
     */
    #isFullPayNow() {
        const totalAmount = this.data.charges.sum(ch => ch.type === 'commission' ? 0 : ch.amount);
        return (this.options.alwaysFullPayCredit && totalAmount <= 0) ||
            (Math.abs(totalAmount) <= this.options.fullPayNowThreshold) ||
            (this.options.alwaysFullPayCancellation && this.data.operation === 'cancellation');
    }

    /**
     * Marks all charges with `immediate` property
     */
    #markAllChargesAsImmediate() {
        for (let ch of this.data.charges) {
            ch.immediate = true;
        }
    }

    /**
     * Finds original and reversal charges that cancel each other out, marking them all as immediate
     */
    #markOriginalAndReversalPairsAsImmediate() {
        for (const ch of this.data.charges)
            ch.groupId = ch.type + ch.perilCharacteristicsLocator + ch.commissionLocator + ch.feeLocator + ch.taxLocator;
        for (const g of Array.from(this.data.charges.groupBy(ch => ch.groupId).values()))
            if (g.length > 1 && Math.abs(g.sum(ch => ch.amount)) < DE_MINIMUS_AMOUNT)
                for (const ch of g)
                    ch.immediate = true;
    }

    /**
     * Marks fee charges with `immediate` property in accordance with options
     */
    #markFeesAsImmediateIfPreferred() {
        if (!this.options.feesOnFirstInstallment) return;

        for (let ch of this.data.charges) {
            if (ch.type === 'fee') {
                ch.immediate = true;
            }
        }
    }

    /**
     * Marks commission charges with `immediate` property in accordance with options
     */
    #markCommissionsAsImmediateIfPreferred() {
        if (!this.options.commissionPayments === 'upFront') return;

        for (let ch of this.data.charges) {
            if (ch.type === 'commission') {
                ch.immediate = true;
            }
        }
    }

    /**
     * Coordinates labeling of charges with `immediate` property as appropriate
     */
    #markImmediateCharges() {
        if (this.#isFullPayNow()) {
            this.#markAllChargesAsImmediate();
        } else {
            this.#markOriginalAndReversalPairsAsImmediate();
            this.#markFeesAsImmediateIfPreferred();
            this.#markCommissionsAsImmediateIfPreferred();
        }
    }

    /**
     * Assigns and refines charges across installments
     * @param terms
     */
    #calcInvoiceItems(terms) {
        for (const term of terms) {
            const chargesInTerm = this.data.charges
                .filter(ch => ch.amount !== 0
                    && ch.coverageStartTimestamp >= term.startTimestamp
                    && ch.coverageStartTimestamp < term.endTimestamp
                    // && (!this.options.installmentFeesFromAuxData || ['fee', 'feeHoldback'].indexOf(ch.type) === -1)
                );


            this.installments = Array(term.installments.length).fill(0);
            let idx = 0;
            for (const ch of chargesInTerm) {
                this.#placeChargeOnInstallments(ch, term.installments, idx === chargesInTerm.length - 1);
                idx++;
            }

            // if (!this.options.adjustAcrossTerms) {
            //     term.installments = this.#carryForwardDeminimis(term.installments);
            //     term.installments = this.#levelInstallments(term.installments);
            // }
        }
    }

    /**
     * Marks installments for removal as appropriate
     * @param installments
     * @param nowTimestamp
     */
    #markEmptyInstallmentsForRemoval(installments, nowTimestamp) {
        for (const inst of installments) {
            if (inst.invoiceItems.length === 0) {
                inst.info.remove = true;
            }
        }

        // Exception for current period installment, which can remain in the final result with empty invoice items.
        // Useful for 'zero-due' invoices as long as rated endorsements require immediate invoice generation.
        let curInst = installments.find(inst => inst.startTimestamp <= nowTimestamp && inst.endTimestamp > nowTimestamp)
            || installments[0];
        if (curInst?.startTimestamp === curInst?.endTimestamp) {
            curInst = installments[1];
        }
        if (curInst) {
            curInst.info.remove = false;

            // SOCA-5486: installments with empty invoice items may interfere with financial transaction mapping,
            //  especially for the immediately-generated endorsement invoice
            if (curInst.invoiceItems.length === 0 && this.data.operation === 'endorsement') {
                // ensure at least one charge on the current period or first installment invoice
                curInst.invoiceItems = [{ chargeId: this.data.charges[0].chargeId, amount: 0 }];
            }
        }
    }

    /**
     * Given an installment, ensures items with matching charge ids are combined into a single entry
     * @param installment
     */
    #combineInvoiceItemsWithSameChargeId(installment) {
        let g = Array.from(installment.invoiceItems.groupBy(ii => ii.chargeId, ii => ii).values());
        installment.invoiceItems = g.map(gg => gg.length === 1 ? gg[0] : {
            chargeId: gg[0].chargeId,
            amount: roundMoney(gg.sum(x => x.amount))
        });
    }

    /**
     * Convenience method to convert string values to numeric types
     */
    #destringifyInstallmentsData() {
        let data = this.data;
        data.policy.originalContractStartTimestamp = parseInt(data.policy.originalContractStartTimestamp);
        data.policy.effectiveContractEndTimestamp = parseInt(data.policy.effectiveContractEndTimestamp);

        for (const m of data.policy.modifications) {
            m.effectiveTimestamp = parseInt(m.effectiveTimestamp);
        }

        for (const ch of data.charges) {
            ch.amount = parseFloat(ch.amount);
            ch.originalAmount = parseFloat(ch.originalAmount);
            ch.previouslyInvoicedAmount = parseFloat(ch.previouslyInvoicedAmount);
            ch.coverageStartTimestamp = parseInt(ch.coverageStartTimestamp);
            ch.coverageEndTimestamp = parseInt(ch.coverageEndTimestamp);
        }

        for (const ch of data.policy.characteristics) {
            ch.policyEndTimestamp = parseInt(ch.policyEndTimestamp);
        }

        for (const inv of data.policy.invoices) {
            inv.startTimestamp = parseInt(inv.startTimestamp);
            inv.endTimestamp = parseInt(inv.endTimestamp);
            inv.totalDue = parseFloat(inv.totalDue);
        }

        for (const pi of data.plannedInvoices) {
            pi.startTimestamp = parseInt(pi.startTimestamp);
            pi.endTimestamp = parseInt(pi.endTimestamp);

            for (let ft of pi.financialTransactions)
                ft.amount = parseFloat(ft.amount);
        }

        data.defaultPaymentTerms.amount = parseInt(data.defaultPaymentTerms.amount);
    }
}

module.exports = {
    InstallmentsGenerator
}