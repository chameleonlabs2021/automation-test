const { DateCalc } = require('../utils/DateCalc.js');
const { roundMoney } = require('../../main/common-options.js').options;
const { durationCalcMethod } = require('../utils/utils.js');

const DEFAULT_OPTIONS = {
    increment: 'wholeDays',
    migrationIndicator: false,
}

class Prorater {
    VERSION = '1.6';

    constructor(data, options = {}) {
        this.data = data;
        this.options = Object.assign({}, DEFAULT_OPTIONS, options);
    }

    getProratedAmounts() {
        let data = this.data;
        this.#destringifyProrationData();

        const policyStartTimestamp = parseInt(data.policy.originalContractStartTimestamp) ||
            this.#fallbackGetEarliest(data.items);

        const dateCalc = new DateCalc(data.tenantTimeZone,
            policyStartTimestamp,
            this.options.increment,
        );

        return {
            items: data.items.map(item => {

                const segmentSplitTimestamp = data.operation === 'cancellation' && data.segmentSplitTimestamp !== item.segmentStartTimestamp ?
                    dateCalc.addToTimestamp(data.segmentSplitTimestamp, 1) : data.segmentSplitTimestamp;

                const holdbackChargeAmount =
                    (
                        this.options.migrationIndicator
                        && this.data.operation === 'cancellation'
                        && ['technicalPremium'].indexOf(item.type) === -1
                    )
                    || (
                        ['Deposit-Dynamic', 'Deposit-Fixed'].indexOf(data.policy.productName) > -1
                        && data.paymentScheduleName === 'upfront'
                        && data.operation === 'cancellation'
                        && ['mid_lease', 'moveout'].indexOf(data.cancellationType?.toLowerCase()) > -1
                        && item.type === 'premium'
                    )
                    // If the cancellation type is one of below, then we should refund the fees (false-positive)
                    || (
                        ['cancel_flat', 'cancel_flat_rewrite', 'lease_not_signed', 'fraud', 'other'].indexOf(data.cancellationType?.toLowerCase()) === -1
                        && item.type === 'fee'
                    )
                    ;

                const holdbackMetadata = this.options.migrationIndicator ? 'Non-refundable premium/fee for migrating policies' : 'Non-refundable policy premium/fee.';

                return {
                    id: item.id,
                    proratedAmount: holdbackChargeAmount ? 0 : roundMoney(dateCalc.getDurationRatio(item.segmentStartTimestamp,
                        // Add 1 day to cancellation date to include the day of cancellation
                        segmentSplitTimestamp,
                        item.segmentEndTimestamp) * item.amount),
                    holdbackAmount: holdbackChargeAmount ? item.amount : 0,
                    holdbackMetadata: holdbackChargeAmount && item.amount > 0 ? holdbackMetadata : undefined,
                }
            })
        };
        //Refund this amount: annual premium * [ 1 -  (cancelation date - policy term start date)/365 ] 

    }

    #fallbackGetEarliest(items) {
        let x = 9999999999999; // Far future date
        for (const i of items)
            x = Math.min(x, i.segmentStartTimestamp);
        return x;
    }

    #destringifyProrationData() {
        let data = this.data;
        data.segmentSplitTimestamp = parseInt(data.segmentSplitTimestamp);
        for (const item of data.items) {
            item.amount = parseFloat(item.amount);
            item.followingAmount = parseFloat(item.followingAmount);
            item.segmentStartTimestamp = parseInt(item.segmentStartTimestamp);
            item.segmentEndTimestamp = parseInt(item.segmentEndTimestamp);
        }
    }
}

module.exports = {
    Prorater
}