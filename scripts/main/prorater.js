//sample script
const { Prorater } = require('../lib/components/Prorater.js');

const global = globalThis;
// To test script uncomment next 2 lines.
// const payload = '{"items":[{"amount":"576.48","fieldValues":{},"followingAmount":"0","id":"2b138c90-e209-4707-9522-a7c28b6070e7_p","perilCharacteristicsLocator":"2b138c90-e209-4707-9522-a7c28b6070e7","perilName":"base_premium","segmentEndTimestamp":"1723420799000","segmentStartTimestamp":"1691827200000","type":"premium"},{"amount":"0.00","fieldValues":{},"followingAmount":"0","id":"2b138c90-e209-4707-9522-a7c28b6070e7_t_3f23f55f-0798-469e-a7d5-036902803fad","perilCharacteristicsLocator":"2b138c90-e209-4707-9522-a7c28b6070e7","perilName":"base_premium","segmentEndTimestamp":"1723420799000","segmentStartTimestamp":"1691827200000","taxLocator":"3f23f55f-0798-469e-a7d5-036902803fad","taxName":"sales","type":"tax"}],"oldPaymentScheduleName":"monthly","operation":"endorsement","paymentPlan":"monthly","paymentScheduleName":"upfront","policy":{"currency":"USD","locator":"101152636","originalContractStartTimestamp":"1691827200000","policyholderLocator":"fd818b63-70ae-4ac2-8e5e-5355664d16cf","productName":"Deposit-Dynamic","quoteLocator":"101152768"},"segmentSplitTimestamp":"1691899200000","tenantTimeZone":"America/New_York"}';
// const payload = '{"cancellationType":"moveout","items":[{"amount":"143.00","fieldValues":{},"followingAmount":"0","id":"fc5e09fd-6882-442f-b8a5-c05796634df5_p","perilCharacteristicsLocator":"fc5e09fd-6882-442f-b8a5-c05796634df5","perilName":"base_premium","segmentEndTimestamp":"1724284800000","segmentStartTimestamp":"1692662400000","type":"premium"}],"oldPaymentScheduleName":"upfront","operation":"cancellation","paymentPlan":"total","paymentScheduleName":"upfront","policy":{"currency":"USD","locator":"101325428","originalContractStartTimestamp":"1692662400000","policyholderLocator":"45fa7c68-fea2-49b2-a335-ce0982089039","productName":"Deposit-Dynamic","quoteLocator":"101325434"},"segmentSplitTimestamp":"1694217600000","tenantTimeZone":"UTC"}';
// const payload = '{"cancellationType":"moveout","items":[{"amount":"1723.00","fieldValues":{},"followingAmount":"0","id":"91115273-045d-4893-a0f1-f58551480d02_p","perilCharacteristicsLocator":"91115273-045d-4893-a0f1-f58551480d02","perilName":"base_premium","segmentEndTimestamp":"1724284799999","segmentStartTimestamp":"1692662400000","type":"premium"}],"oldPaymentScheduleName":"monthly","operation":"cancellation","paymentPlan":"monthly","paymentScheduleName":"monthly","policy":{"currency":"USD","locator":"100201328","originalContractStartTimestamp":"1692662400000","policyholderLocator":"0b95006a-1cd1-442e-9561-e5ae4e440257","productName":"Deposit-Dynamic","quoteLocator":"100201338"},"segmentSplitTimestamp":"1692662400000","tenantTimeZone":"UTC"}';
// const payload = '{"cancellationType":"lapse","items":[{"amount":"0.00","fieldValues":{"coverage_d_loss_of_use_limit":["6000.0"]},"followingAmount":"0","id":"e8415c51-21d0-4331-9c93-5f6a532eea34_p","perilCharacteristicsLocator":"e8415c51-21d0-4331-9c93-5f6a532eea34","perilName":"coverage_d_loss_of_use","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"premium"},{"amount":"0.00","fieldValues":{"coverage_d_loss_of_use_limit":["6000.0"]},"followingAmount":"0","id":"e8415c51-21d0-4331-9c93-5f6a532eea34_tp","perilCharacteristicsLocator":"e8415c51-21d0-4331-9c93-5f6a532eea34","perilName":"coverage_d_loss_of_use","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"technicalPremium"},{"amount":"102.00","fieldValues":{"coverage_c_contents_limit":["20000.0"]},"followingAmount":"0","id":"099c7271-3101-4325-bc0d-d7f58ed31cfc_p","perilCharacteristicsLocator":"099c7271-3101-4325-bc0d-d7f58ed31cfc","perilName":"coverage_c_contents","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"premium"},{"amount":"102.00","fieldValues":{"coverage_c_contents_limit":["20000.0"]},"followingAmount":"0","id":"099c7271-3101-4325-bc0d-d7f58ed31cfc_tp","perilCharacteristicsLocator":"099c7271-3101-4325-bc0d-d7f58ed31cfc","perilName":"coverage_c_contents","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"technicalPremium"},{"amount":"39.00","fieldValues":{"coverage_e_personal_liability_limit":["300000.0"]},"followingAmount":"0","id":"cd75a3e0-d712-4493-b0fe-1cd2d45f16f1_p","perilCharacteristicsLocator":"cd75a3e0-d712-4493-b0fe-1cd2d45f16f1","perilName":"coverage_e_personal_liability","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"premium"},{"amount":"39.00","fieldValues":{"coverage_e_personal_liability_limit":["300000.0"]},"followingAmount":"0","id":"cd75a3e0-d712-4493-b0fe-1cd2d45f16f1_tp","perilCharacteristicsLocator":"cd75a3e0-d712-4493-b0fe-1cd2d45f16f1","perilName":"coverage_e_personal_liability","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"technicalPremium"},{"amount":"0.00","fieldValues":{"coverage_f_medical_payments_limit":["1000.0"]},"followingAmount":"0","id":"52a1df50-7507-4ab9-86df-78bce9273c2b_p","perilCharacteristicsLocator":"52a1df50-7507-4ab9-86df-78bce9273c2b","perilName":"coverage_f_medical_payments","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"premium"},{"amount":"0.00","fieldValues":{"coverage_f_medical_payments_limit":["1000.0"]},"followingAmount":"0","id":"52a1df50-7507-4ab9-86df-78bce9273c2b_tp","perilCharacteristicsLocator":"52a1df50-7507-4ab9-86df-78bce9273c2b","perilName":"coverage_f_medical_payments","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"technicalPremium"},{"amount":"36.00","fieldValues":{"replacement_cost":["yes"]},"followingAmount":"0","id":"27909733-98e2-48e2-b631-7449a44f0297_p","perilCharacteristicsLocator":"27909733-98e2-48e2-b631-7449a44f0297","perilName":"replacement_cost","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"premium"},{"amount":"36.00","fieldValues":{"replacement_cost":["yes"]},"followingAmount":"0","id":"27909733-98e2-48e2-b631-7449a44f0297_tp","perilCharacteristicsLocator":"27909733-98e2-48e2-b631-7449a44f0297","perilName":"replacement_cost","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"technicalPremium"},{"amount":"12.00","fieldValues":{"limited_bed_bug_cover_limit":["0.0"]},"followingAmount":"0","id":"b916d056-bf30-49d3-a132-b3b7c747740f_p","perilCharacteristicsLocator":"b916d056-bf30-49d3-a132-b3b7c747740f","perilName":"limited_bed_bug_cover","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"premium"},{"amount":"12.00","fieldValues":{"limited_bed_bug_cover_limit":["0.0"]},"followingAmount":"0","id":"b916d056-bf30-49d3-a132-b3b7c747740f_tp","perilCharacteristicsLocator":"b916d056-bf30-49d3-a132-b3b7c747740f","perilName":"limited_bed_bug_cover","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"technicalPremium"},{"amount":"35.00","fieldValues":{"personal_electronics_blanket_limit":["1000.0"]},"followingAmount":"0","id":"9a5290fb-fe9f-4fe1-8e38-8affcc6fab7c_p","perilCharacteristicsLocator":"9a5290fb-fe9f-4fe1-8e38-8affcc6fab7c","perilName":"personal_electronics_blanket","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"premium"},{"amount":"35.00","fieldValues":{"personal_electronics_blanket_limit":["1000.0"]},"followingAmount":"0","id":"9a5290fb-fe9f-4fe1-8e38-8affcc6fab7c_tp","perilCharacteristicsLocator":"9a5290fb-fe9f-4fe1-8e38-8affcc6fab7c","perilName":"personal_electronics_blanket","segmentEndTimestamp":"1651795199999","segmentStartTimestamp":"1620259200000","type":"technicalPremium"}],"oldPaymentScheduleName":"monthly","operation":"cancellation","paymentPlan":"monthly","paymentScheduleName":"monthly","policy":{"currency":"USD","locator":"100012762","originalContractStartTimestamp":"1620259200000","policyholderLocator":"df018ee1-8f06-491e-8508-4feb13bde92b","productName":"Protect","quoteLocator":"100012788"},"segmentSplitTimestamp":"1623110399999","tenantTimeZone":"UTC"}';
// global.debug = true;
// console.log(JSON.stringify(getProrationResult(JSON.parse(payload))));


function getProrationResult(data) {
    console.log(`Prorater Plugin - ${data?.policy?.locator}`);
    console.log(JSON.stringify(data));

    // Read test indicator from Aux Data        
    let testIndicator;
    let migrationIndicator;

    if (global?.debug) {
        // testIndicator = true;
        migrationIndicator = !!'true';
    } else {
        testIndicator = socotraApi.getAuxData(data?.policy?.locator, 'test-indicator');
        console.log('Test indicator: ', testIndicator);

        const migrationTimestampString = socotraApi.getAuxData(data?.policy?.locator, 'migration_brightcore_timestamp');
        migrationIndicator = !!socotraApi.getAuxData(data?.policy?.locator, 'migration_indicator');
        console.log('Migration timestamp: ', migrationTimestampString);
        migrationTimestamp = migrationTimestampString ? parseInt(migrationTimestampString) : undefined;
        migrationIndicator = migrationIndicator || migrationTimestamp && dateCalc.getMidDayTimestamp(migrationTimestamp) > Date.now();
        console.log('Migration indicator: ', migrationIndicator);
    }

    const options = {
        migrationIndicator: migrationIndicator,
        ...(testIndicator ? {
            increment: testIndicator === 'hourly' ? 'ms' : 'hours',
        } : undefined),
    };

    const response = (new Prorater(data, options)).getProratedAmounts();
    console.log('Prorater Response: ', JSON.stringify(response));
    return response;
}

exports.getProrationResult = getProrationResult;
