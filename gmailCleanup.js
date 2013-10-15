function markRead() 
{
  var label = GmailApp.getUserLabelByName('flow subscribe');
  var threads = label.getThreads();
      
  for (var i = 0; i < threads.length; i++) 
  {
    
    var messages = threads[i].getMessages();
    
    for (var y=0; y<messages.length; y++) 
    {
      messages[y].markRead();
      Logger.log("Marked Read: " + messages[y].getDate());
      
    }   
  }
}
     
