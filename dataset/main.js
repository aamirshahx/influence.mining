var fs = require('fs')

file = fs.readFileSync('./city_network_min', 'utf8')
fs.writeFileSync('city_network_min_d', file.split('\n').map(v => 'D ' + v).join('\n'))

