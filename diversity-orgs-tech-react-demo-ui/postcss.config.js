const tailwindcss = require('tailwindcss')
module.exports = {
    purge: {
        enabled: true,
        mode: 'all',
        content: [
        './src/**/*/*.jsx',
        './src/**/*/*.js'
    ]
    },
    plugins: [
        tailwindcss('./tailwind.js'),
        require('autoprefixer')
    ]
}
