const { PreGraceAdjuster } = require('../lib/components/PreGraceAdjuster.js');

const global = globalThis;
// To test script uncomment next 2 lines.
// const payload = '{"defaultGracePeriodDays":"15","invoiceLocator":"ad9b8c68-53b3-470b-87a9-6942e77c5074","policy":{"currency":"USD","locator":"100012424","originalContractStartTimestamp":"1620259200000","policyholderLocator":"ff30f93c-b5d0-439b-90c5-04a60b497a90","productName":"Protect","quoteLocator":"100012450"},"tenantTimeZone":"UTC"}';
// global.debug = true;
// console.log(JSON.stringify(getPreGraceResult(JSON.parse(payload))));

function getPreGraceResult(data) {
    console.log(`Pre-Grace Plugin - ${data?.policy?.locator}`);
    console.log(JSON.stringify(data));

    let testIndicator;
    if (!global?.debug) {
        testIndicator = socotraApi.getAuxData(data?.policy?.locator, 'test-indicator');
        console.log('Test indicator: ', testIndicator);
    } else {
        // testIndicator = true;
    }

    const options = {
        ...(testIndicator ? {
            increment: testIndicator === 'hourly' ? 'minutes' : 'hours',
            lookupTable: 'states_cancel_days_test'
        } : {}),
        ...(global?.debug ? {
            cancelEffectiveTimestamp: new Date(2021, 0, 1).getTime(),
        } : {})
    };

    const response = (new PreGraceAdjuster(data, options)).getPreGraceResult();
    console.log('Pre-Grace Response: ', JSON.stringify(response));
    return response;
}

module.exports = {
    getPreGraceResult
}