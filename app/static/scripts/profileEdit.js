require(['./common'], function(common) {
    require(['knockout', 'profile/profileView', 'profile/goal'], function(ko, ProfileView, Goal) {

        ko.applyBindings(new ProfileView());

    });
});
