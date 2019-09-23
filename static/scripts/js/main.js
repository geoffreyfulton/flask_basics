//import { VERSION } from 'lodash';
const _ = require('lodash');


function getLodashVersion() {
    return _.VERSION;
}

document.getElementById('lodashversion').innerHTML = getLodashVersion().toString();