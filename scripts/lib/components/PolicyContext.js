/*
  This class provides methods to easily retreive policy objects
  by locator. By using it plugin scripts can become simpler with
  less repetition.
*/

require('../utils/arrays.js');

class PolicyContext
{
    // We can make #privateMethods after upgrading v8
    constructor(policy)
    {
        this._policy = policy;

        // Maps
        this._exposuresMap = null;
        this._perilsMap = null;
        this._policyModificationsMap = null;
        this._policyCharsMap = null;
        this._exposureCharsMap = null;
        this._perilCharsMap = null;

        // Arrays
        this._allCharacteristics = null;
        this._allPerils = null;
        this._allExposureCharacteristics = null;
        this._allPerilCharacteristics = null;
    }
    getPolicy()
    {
        return this._policy;
    }
    getExposure(locator)
    {
        if (!this._exposuresMap)
        {
            this._exposuresMap =
                this._policy
                    .exposures
                    .toMap(p => p.locator);
        }
        return this._exposuresMap.get(locator);
    }
    getPeril(locator)
    {
        if (!this._perilsMap)
        {
            this._perilsMap =
                this._policy
                    .exposures
                    .flatMap(ex => ex.perils)
                    .toMap(p => p.locator);
        }
        return this._perilsMap.get(locator);
    }
    getPolicyModification(locator)
    {
        if (!this._policyModificationsMap)
        {
            this._policyModificationsMap =
                this._policy
                    .modifications
                    .toMap(m => m.locator);
        }
        return this._policyModificationsMap.get(locator);
    }
    getPolicyCharacteristics(locator)
    {
        if (!this._policyCharsMap)
        {
            this._policyCharsMap =
                this._policy
                    .characteristics
                    .toMap(ch => ch.locator);
        }
        return this._policyCharsMap.get(locator);
    }
    getExposureCharacteristics(locator)
    {
        if (!this._exposureCharsMap)
        {
            this._exposureCharsMap =
                this.allExposureCharacteristics()
                    .toMap(ch => ch.locator);
        }
        return this._exposureCharsMap.get(locator);
    }
    getPerilCharacteristics(locator)
    {
        if (!this._perilCharsMap)
        {
            this._perilCharsMap = this.allPerilCharacteristics()
                                      .toMap(x => x.locator);
        }
        return this._perilCharsMap.get(locator);
    }
    allCharacteristics()
    {
        if (!this._allCharacteristics)
        {
            this._allCharacteristics = 
                this._allCharacteristics ||
                this._policy
                    .characteristics;
        }
        return this._allCharacteristics;
    }
    allExposureCharacteristics()
    {
        if (!this._allExposureCharacteristics)
        {
            this._allExposureCharacteristics = 
                this._allExposureCharacteristics ||
                this._policy
                    .exposures
                    .flatMap(ex => ex.characteristics);
        }
        return this._allExposureCharacteristics;
    }
    allPerils()
    {
        if (!this._allPerils)
        {
            this._allPerils =
                this._policy
                    .exposures
                    .flatMap(ex => ex.perils);
        }
        return this._allPerils;
    }
    allPerilCharacteristics()
    {
        if (!this._allPerilCharacteristics)
        {
            this._allPerilCharacteristics = 
                this._allPerilCharacteristics ||
                this.allPerils()
                    .flatMap(p => p.characteristics);
         }
        return this._allPerilCharacteristics;
    }
    getFieldValue(chars, key)
    {
        return chars.fieldValues[key][0];
    }
    getFieldValueInt(chars, key)
    {
        return parseInt(chars.fieldValues[key][0]);
    }
    getFieldValueFloat(chars, key)
    {
        return parseFloat(chars.fieldValues[key][0]);
    }
    // Timestamps are sent to the plugin in raw string form. This
    // function will convert the timestamps on a characteristics
    // object to numeric form for manipulation, such as by the
    // DateCalc.js library.
    destringifyCharacteristicsTimestamps(chars)
    {
        chars.createdTimestamp = parseInt(chars.createdTimestamp);
        chars.updatedTimestamp = parseInt(chars.updatedTimestamp);
        if (chars.issuedTimestamp)
            chars.issuedTimestamp = parseInt(chars.issuedTimestamp);
        if (chars.replacedTimestamp)
            chars.replacedTimestamp = parseInt(chars.replacedTimestamp);
        if (chars.startTimestamp) // policy or exposure
        {
            chars.startTimestamp = parseInt(chars.startTimestamp);
            chars.endTimestamp = parseInt(chars.endTimestamp);
        }
        else // peril
        {
            chars.coverageStartTimestamp = parseInt(chars.coverageStartTimestamp);
            chars.coverageEndTimestamp = parseInt(chars.coverageEndTimestamp);
        }
    }
    // Field values can be compared by serializing them all to JSON
    // and comparing the strings. We just save the string on the
    // same object for convenience.
    // This depends on the field keys being in the same order.
    getFieldValuesJson(fv)
    {
        return fv.json ||
               (fv.json = JSON.stringify(fv));
    }
}
exports.PolicyContext = PolicyContext;