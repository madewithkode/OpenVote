
/*Dear Aekansh, I Know I'm doing a whole lot of stuffs wrongly, I'm
  not following best practices, I'm writing spaghetti code.
  But trust me,  it got to that point where all i cared was for 
  this shit to run. Do bear with me, hopefully we'll refactor in future.
*/
var enrollmentID; 
var Vote;
var Presidential = ['Divine', 'Chikodi', 'Ladidi','Obinna']; 
var Vice = ['MTN', 'Bishop', 'Asianya', 'Elvis ']; 
var Finsec = ['Judyspiration', 'Ifeoma', 'CBN'];

var Divine = {
    name: 'Divine',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },
};

var Chikodi = {
    name: 'Chikodi',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },
};

var Ladidi = {
    name: 'Ladidi',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },

};

var Obinna = {
    name: 'Obinna',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },

};

var Elvis = {
    name: 'Elvis',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },

};

var MTN = {
    name: 'MTN',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },
};

var Ifeoma = {
    name: 'Ifeoma',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },
};

var Bishop = {
    name: 'Bishop',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },
};

var Judyspiration = {
    name: 'Judyspiration',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },
};

var CBN = {
    name: 'CBN',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },
};

var Asianya = {
    name: 'Asianya',
    department : 'URP',
    level : '300',
    age : '21',
    postInMind : 'Finacial Secreatary',
    totalVotes : 0,
    countMyVotes: function() {
        return this.totalVotes;
    },
    updateVotes: function(){
        this.totalVotes ++;
        return this.totalVotes;
    },
};

function sendVote(voter, candidate, post) {
    //var objectDataString = JSON.stringify(objectData);
    var url = "/update-vote";
    var voterID = voter; 
    var candidateName = candidate;
    var post = post;
    var objectData =
            {
                theVoter: voterID,
                theCandidate: candidateName,
                thePost: post

            };
    $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(objectData),
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);

        }
    });
}   

$(document).ready(function() {
    enrollmentID = sessionID; //i trie to return the voterID using getelementbyID but it didnt work. used a default value
    
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/api/v1/candidates/all", true);
    xhr.send();
    xhr.addEventListener("readystatechange", processRequest, false);
    function processRequest(e) {
        if (xhr.readyState == 4) {
            var response = xhr.responseText;
            console.log(response);
        }
    }

    Vote = function(clicked_id, clicked_class){
        /*get id and class of the clicked vote button which is the aspirant's name and position respectively */
        console.log(clicked_id)
        candidate = clicked_id;
        if (Presidential.includes(candidate)){
            Presidential.splice(Presidential.indexOf(candidate), 1)
            for(var i = 0; i < Presidential.length; i++){
               $('#loader').show();
               $('#'+Presidential[i]).attr('disabled', 'disabled');
               $('#'+Presidential[i]).html('Disabled');
               $('#loader').hide();
               sendVote(enrollmentID, candidate, clicked_class);
               $('#'+candidate).html('Voted');
               $('#'+candidate).attr('disabled', 'disabled');
               console.log(Presidential);
               //$('#'+clicked_id).html('Voted');
            }
        }else if(Vice.includes(candidate)){
            Vice.splice(Vice.indexOf(candidate), 1)
            for(var i = 0; i < Vice.length; i++){
               $('#loader').show();
               $('#'+Vice[i]).attr('disabled', 'disabled');
               $('#'+Vice[i]).html('Disabled');
               $('#loader').hide();
               sendVote(enrollmentID, candidate, clicked_class);
               $('#'+candidate).html('Voted');
               $('#'+candidate).attr('disabled', 'disabled');
               console.log(Vice);
            }    
        }else if(Finsec.includes(candidate)){
            Finsec.splice(Finsec.indexOf(candidate), 1)
            for(var i = 0; i < Finsec.length; i++){
               $('#loader').show();
               $('#'+Finsec[i]).attr('disabled', 'disabled');
               $('#'+Finsec[i]).html('Disabled');
               $('#loader').hide();
               sendVote(enrollmentID, candidate, clicked_class);
               $('#'+candidate).html('Voted');
               $('#'+candidate).attr('disabled', 'disabled');
               console.log(Finsec);
            }
        }
        
        console.log(clicked_class)
        console.log(enrollmentID)
        
    
        


        /*call the candidate object's vote function to do the votin proper*/
        this[candidate].updateVotes();
        console.log(this[candidate].totalVotes) 
        
    }
    
    
    /*Expect less and be surprised by more, expect more and be disappointed by less. 
    it's as simple as that. */
    //This would be the function that would be called by clicking the vote button.
   


})
 
