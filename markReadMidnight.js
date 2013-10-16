//this code should be placed in a google doc on the same Google Apps account as the gmail address as the notifier.
//Create a Google Spreadsheet, click "Tools -> Script Manager -> New"
// Add this code to your function, then go to "Resources -> Current Project Triggers" to set up the schedule
// I set mine as "Time Driven -> Day Timer -> 11pm to midnight", though there are some limitations to this approach

function markReadMidnight() 
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
     
