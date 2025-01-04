module.exports = {
    webpack: function(config, env) {
        // Add CORS headers
        config.devServer = {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
                "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
            }
        };
        return config;
    }
}; 