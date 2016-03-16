/**
 * Created by nishad on 26/02/2016.
 */

function transitionTo(source, destination) {
    $(source).modal("hide");
    $(destination).modal("show");
}

$(document).ready(function () {
    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });

    var canPurchase = true;

    function calculateFundsRequired(event) {
        var sum = 0;

        var balance = $("#items-list").data("balance");


        $.each($(".purchase-amount-slider"), function(key, slider) {
            sum += slider.dataset.itemCost * slider.value;
        });

        if (sum > balance) {
            var element = $("#commit-purchases");
            element.removeClass("btn-success");
            element.addClass("btn-danger");
            element.text("Insufficient Funds");
            canPurchase = false;
        } else {
            var element = $("#commit-purchases");
            element.removeClass("btn-danger");
            element.addClass("btn-success");
            element.text("Submit Purchase(s)");
            canPurchase = true;
        }

        return balance;
    }

    $(".purchase-amount-slider").change(calculateFundsRequired);

    $("#commit-purchases").click(function(event) {
        var items = {};
        var sum = 0;

        var balance = $("#items-list").data("balance");

        $.each($(".purchase-amount-slider"), function(key, slider) {
            items[slider.dataset.itemName] = slider.value;
            sum += slider.dataset.itemCost;
        });

        if (calculateFundsRequired() <= balance) {
            $.post(window.url, JSON.stringify(items), function (data) {
                if (data.success) {
                    if (data.gameover) {
                        console.log("Game over!");
                        window.location.href = data.next;
                    } else {
                        console.log("Completed day.");
                        location.reload();
                    }
                } else {
                    console.log("Failed to update day???")
                }
            }, 'json');
        }

        calculateFundsRequired()
    })
});

// Sourced From: http://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
function getCookie(name) {
    if (document.cookie.length > 0) {
        var start = document.cookie.indexOf(name + "=");
        var end;

        if (start != -1) {
            start = start + name.length + 1;
            end = document.cookie.indexOf(";", start);

            if (end == -1) {
                end = document.cookie.length;
            }

            return unescape(document.cookie.substring(start, end));
        }
    } else {
        return "";
    }
}
