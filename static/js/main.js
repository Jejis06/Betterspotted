function pdref(msg,rand){
        let data =  document.getElementById("commit");
        
        
        if (data.value != "" && data.value != msg )
        {
                send(data,rand);
        }
        else{
          //alert("Invalid message");
          console.log("Invalid message");
        }
          
}
function send(ctx,rand){

      let payload = {
        data : ctx.value,
        verify : parseInt(rand),
      };
      //let payload = ctx.value;
      
      $.post("/recvdata",payload);
     
      //alert("message sent");
      console.log("alert");
      ctx.value = "";
      //window.location.reload(true); 
      //TODO : zaladuj nowy element i tam inne glupoty
}