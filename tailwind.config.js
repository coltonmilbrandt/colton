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
				"theme-color": "#361CC1",
				"theme-color-2": "#FE7A7B",
				"line-theme-color": "#FE7A7B",
				"line-theme-color-2": "#372fca",
				"line-theme-color-3": "#32c7c2",
			},
		},
	},
	variants: {},
	plugins: [],
}
