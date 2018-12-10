var votingHasEnded = false;
var votingCountdown = '';
var votingEnds = '';
var totalVotes = '';
var numberOfAspirants = '';

function endVoting() {
    if(checkVotingHasEnded()){
        votingHasEnded = true;
    }
}

function checkVotingHasEnded() {
    if(votingCountdown == votingEnds){
        return true;
    }else{
        return false;
    }
}