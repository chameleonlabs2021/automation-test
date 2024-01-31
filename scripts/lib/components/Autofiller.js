const { DateCalc } = require("../utils/DateCalc.js");

class Autofiller {
    VERSION = '1.6';

    _dateCalc = null;

    constructor(data) {
        this.data = data;
        if (data.policyLocator) {
            this.policy = socotraApi.fetchByLocator(Policy, data.policyLocator);
            // console.log(`policy: ${JSON.stringify(this.policy)}`);
        }
        this._dateCalc = new DateCalc(data.tenantTimeZone);
    }

    getDataAutofill() {
        const dateCalc = this._dateCalc;
        const data = this.data;
        let autofillResponse = {};

        //const buildingInfo = policy.characteristics.fieldGroupsByLocator[fv.building_details];
        //const state = policy.characteristics[policy.characteristics.length - 1].fieldGroupsByLocator[fv.building_details]?.address_state

        switch (data.operation) {
            case 'newBusiness':
                // logic to augment new business response
                if (data.operationType === 'create') {
                    autofillResponse = {
                        ...(!data.updates.fieldValues.policy_term || data.updates.fieldValues.policy_term[0] === '0' ? this.#incrementPolicyTerm(data, 1, true) : {}),
                        ...this.#adjustPolicyEndTimestamp(data),
                    };
                } else if (data.operationType === 'update') {
                    autofillResponse = this.#rewritePolicy(data) ?? autofillResponse;
                }
                break;
            case 'endorsement':
                // logic to augment  update response                
                autofillResponse = this.#incrementPolicyTerm(data, 0.1);
                break;
            case 'renewal':
                // const pc = this.policy.characteristics[this.policy.characteristics.length - 1];

                // logic to augment update response
                autofillResponse = {
                    ...this.#incrementPolicyTerm(data),
                    // "renewalStartTimestamp": dateCalc.getStartOfDayTimestamp(parseInt(pc.policyEndTimestamp) + 1000),
                    ...this.#adjustPolicyEndTimestamp(data),
                };
                break;
            default:
                // logic to augment update response
                break;
        }
        return autofillResponse;
    }

    #incrementPolicyTerm(data, incrementBy = 1, overridePolicyTerm = false) {
        let policyTerm = incrementBy;
        if (!overridePolicyTerm) {
            const fv = this.policy.characteristics[this.policy.characteristics.length - 1].fieldValues;
            policyTerm = fv.policy_term[0];
            console.log(`policyTerm: ${policyTerm}`);
        }

        return {
            fieldValues: {
                "policy_term": overridePolicyTerm ? policyTerm : Math.floor((parseFloat(policyTerm) + incrementBy) * 1000) / 1000,
                // policyEndTimestamp = data.updates.policyEndTimestamp,
            }
        };
    }

    #adjustPolicyEndTimestamp(data) {
        if (!data?.updates) return {};
        const dateCalc = this._dateCalc;
        const policyStartTimestamp = parseInt(data.updates.policyStartTimestamp);
        const policyEndTimestamp = parseInt(data.updates.policyEndTimestamp);
        const sameDay = dateCalc.toMoment(policyStartTimestamp).date() === dateCalc.toMoment(policyEndTimestamp).date();

        return {
            "policyEndTimestamp": sameDay ? dateCalc.getStartOfDayTimestamp(policyEndTimestamp) - 1 : dateCalc.getEndOfDayTimestamp(policyEndTimestamp)
        };
    }

    #rewritePolicy(data) {
        const previousPolicyId = data.updates.fieldValues.previous_policy_locator;
        console.log(`previousPolicyId: ${previousPolicyId}`);
        if (!previousPolicyId) return {
            ...this.#adjustPolicyEndTimestamp(data),
        };

        const policy = socotraApi.fetchByLocator(Policy, previousPolicyId);
        // console.log(`policy: ${JSON.stringify(policy)}`);

        let addExposures = [];
        if (policy.exposures.length > 0) {
            for (let exposure of policy.exposures) {
                let addPerils = [];
                for (let peril of exposure.perils) {
                    addPerils.push({
                        "name": peril.name,
                        "fieldValues": peril.characteristics[peril.characteristics.length - 1].fieldValues
                    })
                }
                addExposures.push({
                    "exposureName": exposure.name,
                    "perils": addPerils,
                    "fieldGroups": [],
                    "fieldValues": exposure.characteristics[exposure.characteristics.length - 1].fieldValues
                })
            }
        }

        const pc = policy.characteristics[policy.characteristics.length - 1];

        const fieldGroups = [
            "addl_interests",
            "building_details",
            "non_primary_policy_holders",
        ]
        const addFieldGroups = [];
        fieldGroups.forEach(fieldGroupName => {
            pc.fieldValues[fieldGroupName]?.forEach(locator => {
                if (!pc.fieldGroupsByLocator[locator]) return;
                addFieldGroups.push({
                    fieldName: fieldGroupName,
                    fieldValues: pc.fieldGroupsByLocator[locator],
                });
            });
        });

        const autofillResponse = {
            ...this.#adjustPolicyEndTimestamp(data),
            "paymentScheduleName": policy.paymentScheduleName,
            "fieldValues": {
                ...pc.fieldValues,
                "addl_interests": [],
                "building_details": [],
                "non_primary_policy_holders": [],
                "previous_policy_start_date": pc.policyStartTimestamp,
                "rewritten": "true",
            },
            "addFieldGroups": addFieldGroups,
            "addExposures": addExposures,
        }
        return autofillResponse;

    }
}

module.exports = {
    Autofiller
}