// Configuration file for tool URLs
// Edit the URLs below to point to your tools

const TOOL_URLS = {
    // Switch Comparison Tool
    'switch-comparison': 'https://engswitches-mp7x.vercel.app/switch_comparison_web.html',

    // Camera AI Token Calculator
    'camera-calculator': 'https://tokens-ia.vercel.app/',

    // Switch EnGenius Filter (local)
    'switch-filter': 'https://switchesengenius.vercel.app/',

    // Access Point Comparison Tool
    'ap-comparison': 'https://eng-theta.vercel.app/'
};

// Export for use in home.html
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TOOL_URLS;
}
