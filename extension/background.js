// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "translated_image"){
      // console.log(message)
      sendResponse(message)
    }
  });
  