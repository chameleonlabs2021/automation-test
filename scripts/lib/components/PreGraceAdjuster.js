/**
 * Basic pre-grace adjustment sample: simply adds a set number of days
 * to current time, setting the result as the new grace period end timestamp
 * and the cancellation effective timestamp as midnight of the new grace period end timestamp.
 *
 * You can adopt this plugin as-is and set the options on instantiation if this
 * behavior suits your needs; else, you will need to override preGraceResult with more complex
 * logic.
 */
const { DateCalc } = require('../utils/DateCalc.js');

const global = globalThis;
const DEFAULT_OPTIONS = {
    additionalDaysGrace: 30, // additional days beyond now
    cancelEffectiveTimestamp: new Date().getTime(), // base timestamp to use instead of now
    increment: 'days',
    lookupTable: 'states_cancel_days',
}

class PreGraceAdjuster {
    VERSION = '1.6';

    constructor(data, options = {}) {
        this.data = data;
        this.options = Object.assign({}, DEFAULT_OPTIONS, options);
    }

    getPreGraceResult() {
        console.log("Grace Plugin Fired");
        const data = this.data;
        try {
            let invoiceStartTimestamp = undefined;
            let state_grace_days = undefined;

            if (!global?.debug) {
                //Find the state
                const policy = socotraApi.fetchByLocator(Policy, data.policy.locator);
                const fv = policy.characteristics[policy.characteristics.length - 1].fieldValues;
                const state = policy.characteristics[policy.characteristics.length - 1].fieldGroupsByLocator[fv.building_details]?.address_state
                console.log("State: " + state);
                
                //Find the value of days for the state
                console.log("Lookup table: " + this.options.lookupTable);
                state_grace_days = socotraApi.tableLookup(0, this.options.lookupTable, state);
                console.log("State grace days: " + state_grace_days);
                                
                //Find start date of the unpaid invoice
                const invoice = socotraApi.fetchByLocator(Invoice, data.invoiceLocator);
                invoiceStartTimestamp = invoice?.startTimestamp? parseInt(invoice.startTimestamp) : undefined;
                console.log("Invoice start timestamp: " + invoiceStartTimestamp ?? "No invoice start timestamp found");
            }

            //Apply days to Grace period
            const cancelEffectiveTimestamp = invoiceStartTimestamp ?? this.options.cancelEffectiveTimestamp ?? new Date().getTime();
            const dateCalc = new DateCalc(data.tenantTimeZone);
            const newGraceEndTimestamp = dateCalc.addToTimestamp(
                cancelEffectiveTimestamp,
                state_grace_days ?? this.options.additionalDaysGrace,
                this.options.increment,
            );

            console.log(`Grace period end timestamp: ${newGraceEndTimestamp}`);
            console.log(`Cancel effective timestamp: ${cancelEffectiveTimestamp}`);

            return {
                gracePeriodEndTimestamp: newGraceEndTimestamp,
                cancelEffectiveTimestamp: dateCalc.getEndOfDayTimestamp(cancelEffectiveTimestamp),
            };
        }
        catch (error) {
            console.log(`Error in Pre-Grace Plugin: ${error}`);
            return {};
        }
    }
}

module.exports = {
    PreGraceAdjuster
}