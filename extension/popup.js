document.getElementById("takeScreenshotBtn").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const activeTab = tabs[0];
    chrome.tabs.captureVisibleTab({ format: "jpeg", quality: 100 }, (dataUrl) => {
      // console.log(dataUrl)
      // console.log(activeTab)
      chrome.sidePanel.open({
        tabId:activeTab.id
      });
      $.ajax({ 
        url: 'http://127.0.0.1:5000/translate', 
        type: 'POST', 
        data: {"image":dataUrl.slice(dataUrl.indexOf(',')+1)},
        success: function(response){ 
          
            chrome.runtime.sendMessage({action:"translated_image", translated_image_data: response, tabid: activeTab.id});
        } 
    })
    });
  });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action == "translated_image"){
    // console.error("I received it")
    document.getElementById("image").src = "data:image/jpeg;base64,"+message.translated_image_data
    document.getElementById("display_result").style.display = "block"
    document.getElementById("loading_result").style.display = "none"
  }
});
