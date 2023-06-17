// session-persistence.js

// Configure session persistence
firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION)
    .then(function() {
        // Session persistence is now set
    })
    .catch(function(error) {
        // Handle error
    });
