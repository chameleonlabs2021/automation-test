/**
 * Sample underwriter plugin. Override getUnderwritingResults for your own implementation.
 */
require('../utils/arrays.js');
const { parseValue } = require('../utils/utils.js');
const { PolicyContext } = require('./PolicyContext.js');

class Underwriter {
    VERSION = '1.6';

    constructor(data) {
        this.data = data;
    }

    getUnderwritingResults() {
        const data = this.data;
        const context = new PolicyContext(data.policy);
        const policyHolderFull = data.policyholder;
        const policyHolder = this.#parsePolicyHolderKeys(policyHolderFull.entity.values);

        let decision = 'accept';
        let notes = [];

        /**
         * Pattern: base decisions on any relevant data at policy, exposure, peril level
         */
        // Policy
        const policy = context.getPolicy();
        const policyResults = this.getDecisionAndNotesForPolicyChars(this.#getUnreplaced(policy.characteristics));

        //Policyholder
        const policyholderResults = this.getDecisionAndNotesForPolicyholderChars(policyHolder);

        // Exposures
        const expResults = this.getDecisionAndNotesForExposureChars(
            this.#getUnreplaced(context.allExposureCharacteristics()));

        // Perils
        const perilResults = this.getDecisionAndNotesForPerils(
            this.#getUnreplaced(policy.characteristics),
            this.#getUnreplaced(context.allPerils()));

        const decisions = [policyResults, expResults, perilResults, policyholderResults].map(r => r.decision);
        if (decisions.includes('none')) {
            decision = 'none';
        }

        if (decisions.includes('reject')) {
            decision = 'reject';
        }

        notes = [...policyResults.notes,
        ...expResults.notes,
        ...perilResults.notes,
        ...policyholderResults.notes];

        return { decision, notes };
    }

    /**
     * Return a decision and notes pertaining to policy characteristics.
     *
     * @param policyCharacteristics the set of unreplaced policy characteristics
     */
    getDecisionAndNotesForPolicyChars(policyCharacteristics) {
        let decision = 'accept';
        let notes = [];
        // const policyCh = parseValue(policyCharacteristics);

        let states = ['IN'];

        for (const policyCh of policyCharacteristics) {

            // Product based rules
            switch (this.data.policy.productName) {
                case 'Deposit-Fixed':
                    // if (!(
                    //     this.data.operation === 'renewal'
                    //     || parseValue(policyCh.fieldGroupsByLocator[parseValue(policyCh.fieldValues?.building_details)]?.address_state)?.toUpperCase() === 'CA'
                    // )) {
                    //     decision = 'reject';
                    //     notes.push('This product is only available in California.');
                    // }

                    if (parseValue(policyCh.fieldValues?.credit_score)?.toLowerCase() === 'deceased') {
                        decision = 'reject';
                        notes.push('Policy cannot be issued for a deceased person.');
                    }

                    break;

                case 'Deposit-Dynamic':

                    if (parseValue(policyCh.fieldValues.credit_score)?.toLowerCase() === 'deceased') {
                        decision = 'reject';
                        notes.push('Policy cannot be issued for a deceased person.');
                    }

                    break;

                case 'Protect':

                    states.push('FL', 'NC', 'MO');

                    const iso_protection_class = parseValue(policyCh.fieldGroupsByLocator[parseValue(policyCh.fieldValues?.building_details)]?.iso_protection_class);
                    if (['new_business', 'endorsement'].indexOf(this.data.operation) > -1 && (iso_protection_class?.startsWith("9") || iso_protection_class?.startsWith("10"))) {
                        decision = 'reject';
                        notes.push('Protection class can not be 9 or 10');
                    }
            }

            // Common rules
            if (states.indexOf(parseValue(policyCh.fieldGroupsByLocator[parseValue(policyCh.fieldValues?.building_details)]?.address_state)?.toUpperCase()) > -1) {
                decision = 'reject';
                notes.push(`Following states are not available - ${states.join(', ')}`);
            }
        }

        return { decision, notes };
    }

    getDecisionAndNotesForPolicyholderChars(policyholder) {
        let decision = 'accept';
        let notes = [];
        // PolicyHolder decisions and notes
        //if(parseValue(policyholder.date_of_birth))

        const dob = parseValue(policyholder.date_of_birth);

        if (dob !== null && calculateAge(dob) < 18) {
            decision = 'reject';
            notes.push('Individual must be at least 18 years old.');
        }

        // Removed OFAC check - https://synpulse-org.slack.com/archives/C04TAVD8ETY/p1691154320172439?thread_ts=1691146698.280949&cid=C04TAVD8ETY
        // console.log(parseValue(policyholder.ofac_outcome));
        // if (parseValue(policyholder.ofac_outcome)?.toLowerCase() === "step up") {
        //     decision = 'reject';
        //     notes.push('OFAC cannot be negative.');
        // }
        return { decision, notes };
    }

    /**
     * Return a decision and notes pertaining to exposure characteristics
     * @param exposureCharacteristics the set of unreplaced exposure characteristics
     */
    getDecisionAndNotesForExposureChars(exposureCharacteristics) {
        let decision = 'accept';
        let notes = [];
        for (const exposureCh of exposureCharacteristics) {
            // Policy decisions and notes
            if (parseValue(exposureCh.fieldValues.bond_amount) === null || parseValue(exposureCh.fieldValues.bond_amount) >= 25000) {
                decision = 'reject';
                notes.push('Bond amount must be less than 25,000');
            }
        }

        return { decision, notes };
    }

    getDecisionAndNotesForPerils(policyCharacteristics, perils) {
        let decision = 'accept';
        let notes = [];
        const policyCh = parseValue(policyCharacteristics, null, policyCharacteristics.length - 1);
        for (const peril of perils) {
            if (peril.name === 'il_mine_subsidence'
                && parseValue(policyCh.fieldGroupsByLocator[parseValue(policyCh.fieldValues?.building_details)]?.address_state)?.toUpperCase() != 'IL') {
                decision = 'reject';
                notes.push('Il mine subsidence is not available outside Illinois');
            }
        }

        return { decision, notes };
    }

    /**
     * Return a decision and notes pertaining to peril characteristics
     * @param perilCharacteristics the set of unreplaced peril characteristics
     */
    getDecisionAndNotesForPerilChars(perilCharacteristics) {
        let decision = 'accept';
        let notes = [];
        for (const perilCh of perilCharacteristics) {
            // Peril decisions and notes
        }

        return { decision, notes };
    }

    #getUnreplaced(chars) {
        return chars.filter(ch => !ch.replacedTimestamp);
    }

    #parsePolicyHolderKeys(policyHolder) {
        const policyHolderKeys = {};
        for (const key in policyHolder) {
            policyHolderKeys[key.split("_").slice(2).join("_")] = policyHolder[key]?.value;
        }
        return policyHolderKeys;
    }
}

function calculateAge(dob) { // dob is a string in format YYYYMMDD
    if (!dob) return dob;
    const birthday = dob.indexOf('-') === -1 && dob.length === 8 ? new Date(dob.substr(0, 4), dob.substr(4, 2) - 1, dob.substr(6, 2)) : new Date(dob);
    const ageDifMs = Date.now() - birthday;
    const ageDate = new Date(ageDifMs); // miliseconds from epoch
    return ageDate.getUTCFullYear() - 1970;
}

module.exports = {
    Underwriter
}