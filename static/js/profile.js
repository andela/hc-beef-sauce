$(function() {

    $(".member-remove").click(function() {
        var $this = $(this);

        $("#rtm-email").text($this.data("email"));
        $("#remove-team-member-email").val($this.data("email"));
        $('#remove-team-member-modal').modal("show");

        return false;
    });

});

$(function() {
    $(".priority-edit").click(function() {
        var $this = $(this);

        $("#user-email").text($this.data("email"));
        $("#edit-priority-user").val($this.data("email"));
        $("#priority-edit-team-member-modal").modal("show");
        
        return False
    });
});

$(function() {
    $(".check-remove").click(function() {
        var $this = $(this);

        $("#rtm-user").text($this.data("user"));
        $("#remove-team-member-user").val($this.data("user"));
        $("#rtm-name").text($this.data("name"));
        $("#remove-team-member-name").val($this.data("name"));
        $("#rtm-code").text($this.data("code"));
        $("#remove-team-member-code").val($this.data("code"));
        $('#remove-team-member-check-modal').modal("show");

        return false;
    });

});
