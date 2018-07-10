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
    })
})