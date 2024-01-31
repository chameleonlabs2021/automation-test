module.exports = {
    durationCalcMethod: (paymentScheduleName) => (paymentScheduleName === 'weekly' ? 'wholeDays' : 'months'),
    parseValue: (value, type = 'array', index = 0) => {
        if (value === undefined || value === null) return value;
        const parsedValue = value && Array.isArray(value) ? value[index] : value;
        switch (type) {
            case 'select':
                return parsedValue === 'yes' ? true : false;
            case 'boolean':
                return parsedValue ? 'yes' : 'no';
            case 'number':
                return +parsedValue;
            default:
                return parsedValue;
        }
    }
}