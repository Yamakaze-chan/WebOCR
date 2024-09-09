chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action == "translated_image"){
      // console.error("I received it")
      document.getElementById("image").src = "data:image/jpeg;base64,"+message.translated_image_data
      document.getElementById("display_result").style.display = "block"
      document.getElementById("loading_result").style.display = "none"
    }
  });