var Emma = {
    name: 'Emma',
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
    }
};

/*Expect less and be surprised by more, expect more and be disappointed by less. 
it's as simple as that. */