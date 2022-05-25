const Instagram = require('instagram-web-api');
require("dotenv").config();
const argv = process.argv.slice(2);

const client = new Instagram({
    username: argv[0],
    password:argv[1],
    
    }
);


;(async () => {
    await client.login()
    const profile = await client.getProfile()
    if (profile === undefined) {
        console.log(1)
    }
    else
        console.log(profile)
  })()