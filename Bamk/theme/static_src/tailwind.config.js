module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                navy: "#03045F",
                deepblue: "#0078B8",
                skyblue: "#00B6DA",
                lightblue: "#93E1F0",
                paleblue: "#CEF1F9"
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
};
