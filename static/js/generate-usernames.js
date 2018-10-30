const baseUrl = 'https://username-generation-api.herokuapp.com/api?';
$(document).ready(() => {
    $('#usernames-form').submit((event) => {
        event.preventDefault();
        let errors = [];
        let usernameDiv = $('#username-results');

        let requestParams = {};
        requestParams.min_length = $('#min_length').val();
        requestParams.max_length = $('#max_length').val();
        requestParams.use_underscores = $('#use_underscores').is(':checked');
        requestParams.amount = $('#amount').val();

        let url = baseUrl + $.param(requestParams);
        $.ajax({
            url: url,
            success: (result) => {
                let usernamesArray = result['usernames'];
                usernameDiv.html('');
                usernamesArray.forEach((username) => usernameDiv.append(username + '<br/>'));
            },
            error: (error) => {
                // something went wrong
                if (error['responseJSON']['errors']) {
                    errors = error['responseJSON']['errors'];
                } else {
                    errors.push('There was an unspecified error. Please try again.');
                }

                usernameDiv.html('');
                errors.forEach((error) => usernameDiv.append(error + '<br/>'));
            }
        });
    });
});
