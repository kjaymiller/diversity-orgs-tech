const tailwindcss = require('tailwindcss')
module.exports = {
    purge: {
        enabled: true,
        content: [
        './src/**/*.jsx',
        './src/**/*.js'
    ]
    },
    plugins: [
        tailwindcss('./tailwind.js'),
        require('autoprefixer')
    ]
}
