
const Instagram = require('instagram-web-api');
const FileCookiesStore = require("tough-cookie-filestore2");
require("dotenv").config();


const argv = process.argv.slice(2);


const cookieStore = new FileCookiesStore("./cookies.json");

const client = new Instagram({
    username: process.env.LOG,
    password:process.env.PAS,
    cookieStore,
    }
);

const instagramPOST = async (photo) =>{

    await client.uploadPhoto({
        photo: photo,//"https://i.wpimg.pl/730x0/m.fotoblogia.pl/jajko-688cda13e203b23850b3998237.jpg",
        post:"feed",
    }).catch((err) => {
        console.log(`[ERROR : ${err}]`);
    }).then( (res) =>{
        console.log(`[UPLOADED PHOTO : https://www.instagram.com/p/${res.media.code}]`);

        
    });
};

client.login().then(async ()=>{
    console.log("[LOGGED IN]");
    
    for (let index = 0; index < argv.length; index++) {
        const photo = argv[index];       
        await instagramPOST(photo);
    }
    
});
