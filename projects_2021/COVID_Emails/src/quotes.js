/*
 * Creates tooltip with provided id that
 * floats on top of visualization.
 * Most styling is expected to come from CSS
 * so check out bubble_chart.css for more details.
 */
function listOfQuotes(listId, quotes) {
  // Local variable to hold tooltip div for
  // manipulation in other functions.

  function showQuote(d) {
    var word = d.name;
    var leftcol = document.getElementById('quotes').getElementsByClassName("column")[0];
    var rightcol = document.getElementById('quotes').getElementsByClassName("column")[1];

    var i, j, wordInfo, wordInfoArray, numEmails, numSentences, sender, email, sentencesArray, sentences, HTMLcode;
    wordInfo = quotes[word];
    if (!Array.isArray(wordInfo)) {
      wordInfoArray = new Array(wordInfo);
    } else {
      wordInfoArray = wordInfo
    }
    numEmails = Math.min(wordInfo.length, 10);

    console.log(d.count_HOCs);
    console.log(Math.round(d.count_HOCs));
    leftcol.innerHTML = "<center><h2>HOCs mentioned <markleft>" + word + "</markleft> " + Math.round(d.count_HOCs) + "<br>times per 25k words</h2></center>";
    rightcol.innerHTML = "<center><h2>Admin mentioned <markright>" + word + "</markright> " + Math.round(d.count_admin) + "<br>times per 25k words</h2></center>";
    for (i = 0; i < numEmails; i++) {
      HTMLcode = "";
      sender = wordInfo[i]['sender'];
      email = wordInfo[i]['email'];
      sentences = wordInfo[i]['sentences'];
      if (!Array.isArray(sentences)) {
        sentencesArray = new Array(sentences);
      } else {
        sentencesArray = sentences
      }
      
      numSentences = Math.min(sentencesArray.length, 3);

      HTMLcode += "<blockquote cite=\"" + email + "\">";
      var regEx = new RegExp(word, "ig");
      for (j = 0; j < numSentences; j++) {
        console.log(sentencesArray[j]);
        HTMLcode += "<p>" + sentencesArray[j].replace(regEx, "<ABCZYX>" + word + "</ABCZYX>") + "</p>";
      }
      HTMLcode += "</blockquote>";

      console.log(sender);
      if (sender == "HOCs") {
        leftcol.innerHTML += HTMLcode.replace(/ABCZYX/g, "markleft");
      } else {
        rightcol.innerHTML += HTMLcode.replace(/ABCZYX/g, "markright");
      }
    }
  }

  function hideQuote() {
    var leftcol = document.getElementById('quotes').getElementsByClassName("column")[0];
    var rightcol = document.getElementById('quotes').getElementsByClassName("column")[1];
    leftcol.innerHTML = "";
    rightcol.innerHTML = "";
  }

  return {
    showQuote: showQuote,
    hideQuote: hideQuote
  };
}
