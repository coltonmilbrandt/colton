module.exports = {
	content: [
		"./components/**/*.{html,js}",
		"./pages/**/*.{html,js}",
		"./index.html",
	],
	theme: {
		extend: {
			inset: {
				100: "100%",
			},

			padding: {
				120: "120px",
			},

			colors: {
				"theme-color": "#142D49",
				"theme-color-2": "#355C76",
				"line-theme-color": "#355C76",
				"line-theme-color-2": "#3C8B88",
				"line-theme-color-3": "#809AA6",
			},
		},
	},
	variants: {},
	plugins: [],
}
