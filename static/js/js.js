$(document).ready(() => {
    // Getting number of days for a given leave type
    $("#leave_type").change(() => {
        leave_type = document.querySelector('#leave_type').value;

        $.ajax({
            type: 'get',
            url: configuration['leave']['get_no_of_days'],
            data: { 'leave_type': leave_type },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#no_days').value = data.no_of_days;
                    if (data.leave == "Annual") {
                        document.querySelector('#no_days').readOnly = false;
                    } else {
                        document.querySelector('#no_days').readOnly = true;
                    }
                } else {}
            },

        });
    });

    // Getting Leave End date
    $("#st_date").change(() => {
        start_date = document.querySelector('#st_date').value;
        no_days = document.querySelector('#no_days').value;

        $.ajax({
            type: 'get',
            url: configuration['leave']['get_end_date'],
            data: { 'startDate': start_date, 'no_of_days': no_days },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#end_date').value = data.end_date;
                } else {
                    // alert(data.message);
                }

            },

        });
    });

    // Approving/rejecting Leave Application
    $("#submit_leave_application").click(() => {
        var selected = $("#select_action :selected").text();
        application_id = document.querySelector('#application_id').value;

        switch (selected) {
            case "Approve":
                var form_data = $("#leave_form").serialize();

                $.ajax({
                    type: 'POST',
                    url: configuration['leave']['approve_leave'],
                    data: form_data,
                    dataType: 'json',
                    success: (data) => {
                        window.location.href = configuration['leave']['leave_dashboard_page'];
                    }
                });
                break;
            case "Reject":
                var form_data = $("#leave_form").serialize();

                $.ajax({
                    type: 'POST',
                    url: configuration['leave']['reject_leave'],
                    data: form_data,
                    dataType: 'json',
                    success: (data) => {
                        window.location.href = configuration['leave']['leave_dashboard_page'];
                    }
                });
                break;
            default:
        }
    })

    // Editing Leave application
    $("#edit_leave_btn").click(() => {
        var form_data = $("#edit_leave_form").serialize();
        $.ajax({
            type: 'POST',
            url: configuration['leave']['edit_leave_application'],
            data: form_data,
            dataType: 'json',
            success: (data) => {
                window.location.href = configuration['leave']['apply_leave_page'];
            }
        });
    })

    // Deleting Leave application
    $("#delete_leave_btn").click(() => {
        $.ajax({
            type: 'POST',
            url: configuration['leave']['delete_leave_application'],
            data: form_data,
            dataType: 'json',
            success: (data) => {
                window.location.href = configuration['leave']['apply_leave_page'];
            }
        });
    })

    // Save Employee Contact
    $("#contact_submit").click(() => {
        var form_data = $("#contact_form").serialize();
        $.ajax({
            type: 'POST',
            url: configuration['employees']['add_employee_contacts'],
            data: form_data,
            dataType: 'json',
            success: (data) => {
                location.reload();
            }
        });
    })

    // Delete Employee Contact
    $("#contact_delete").click(() => {
        var contact_id = document.querySelector('#contact_id').value;
        $.ajax({
            type: 'get',
            url: configuration['employees']['delete_employee_contact'],
            data: { "contact_id": contact_id },
            dataType: 'json',
            success: (data) => {
                location.reload();
            }
        });
    })
});