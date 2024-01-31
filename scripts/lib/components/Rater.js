/**
 * Sample rater implementation - override getRatedAmounts in your own implementation.
 */
require("../utils/arrays.js");
const { DateCalc } = require("../utils/DateCalc.js");
const { PolicyContext } = require("./PolicyContext.js");
const { durationCalcMethod } = require('../utils/utils.js');
const { roundMoney } = require('../../main/common-options.js').options;

const global = globalThis;
const DEFAULT_OPTIONS = {
    // Default options
    // Peril rates from aux data
    perilRates: undefined,
}

class Rater {
    VERSION = '1.6';

    data;
    options;

    constructor(data, options = {}) {
        this.data = data;
        this.options = {
            ...{},
            ...DEFAULT_OPTIONS,
            ...options
        };
        console.log('Rater Options: ', JSON.stringify(this.options));
    }

    getRatedAmounts() {
        let data = this.data;

        const dateCalc = new DateCalc(data.tenantTimeZone,
            parseInt(data.policy.originalContractStartTimestamp),
            durationCalcMethod(data.policy.paymentScheduleName));

        const context = this.preprocessContext(new PolicyContext(data.policy));
        const charsToRate = data.policyExposurePerils.map(
            pep => context.getPerilCharacteristics(pep.perilCharacteristicsLocator));

        const auxDataSuffix = `${this.#resolvePolicyTerm()?.replace('.', '-')}`;
        console.log('Aux Data Suffix: ', auxDataSuffix);

        const perilRatesString = global?.debug ?
            this.options.perilRates : socotraApi.getAuxData(this.data?.policy?.locator, `migration_policy_premium_${auxDataSuffix}`);
        console.log('Policy Premium from Aux Data: ', `migration_policy_premium_${auxDataSuffix}`);
        console.log('Policy Premium Data: ', perilRatesString);

        const perilRates = JSON.parse(perilRatesString);
        const rates = {};

        for (const ch of charsToRate) {
            // Iterate over characteristics, using peril, exposure, and policy data to set factors and perform calcs
            const peril = context.getPeril(ch.perilLocator);
            const rate = perilRates[peril.name];
            const premium = roundMoney(rate);

            rates[ch.locator] = {
                exactPremium: premium,
                yearlyPremium: rate,
                yearlyTechnicalPremium: rate,
            };
        }

        return {
            pricedPerilCharacteristics: rates,
            exceptionMessage: undefined,
        };
    }

    preprocessContext(context) {
        for (const perCh of context.allPerilCharacteristics()) {
            perCh.coverageStartTimestamp = parseInt(perCh.coverageStartTimestamp);
            perCh.coverageEndTimestamp = parseInt(perCh.coverageEndTimestamp);
        }
        return context;
    }

    #resolvePolicyTerm() {
        const pc = new PolicyContext(this.data.policy);
        const chars = pc.allCharacteristics();
        // TODO: Change to getFieldValueFloat once resolved from Coherent rater
        const policyTerm = pc.getFieldValue(chars[chars?.length - 1], 'policy_term');

        return policyTerm;
    }
}

module.exports = {
    Rater
}