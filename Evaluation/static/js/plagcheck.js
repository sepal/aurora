

load_plagcheck_diff = function (suspect_txt, similar_txt) {

    document.getElementById('similar_orig').innerHTML = similar_txt;
    document.getElementById('suspect_orig').innerHTML = suspect_txt;

    var diff = JsDiff.diffWords(suspect_txt, similar_txt);

    var similar_processed = document.getElementById('similar_processed');
    var suspect_processed = document.getElementById('suspect_processed');

    diff.forEach(function(part, i){
        if (!part.removed && !part.added) {
            if (part.value.match(/^[\s,\.]*$/)) {
                similar_processed.innerHTML += part.value;
                suspect_processed.innerHTML += part.value;
            } else {
                similar_processed.innerHTML += '<span class="diff_part" id="similar_part_' + i + '">' + part.value + '</span>';
                suspect_processed.innerHTML += '<span class="diff_part" id="suspect_part_' + i + '">' + part.value + '</span>';
            }
        } else if (!part.removed && part.added) {
            similar_processed.innerHTML += part.value;
        } else if (part.removed && !part.added) {
            suspect_processed.innerHTML += part.value;
        }
    });
};

$(function() {
    $('#show_suspect_orig').change(function() {
        if (this.checked) {
            $('#suspect_processed').addClass("text_disabled");
            $('#suspect_orig').removeClass("text_disabled");
        } else {
            $('#suspect_processed').removeClass("text_disabled");
            $('#suspect_orig').addClass("text_disabled");
        }
    });
});

$(function() {
    $('#show_similar_orig').change(function() {
        if (this.checked) {
            $('#similar_processed').addClass("text_disabled");
            $('#similar_orig').removeClass("text_disabled");
        } else {
            $('#similar_processed').removeClass("text_disabled");
            $('#similar_orig').addClass("text_disabled");
        }
    });
});

$(function() {
    $(".diff_part").on( "mouseenter mouseleave", function(event) {
        var id_str = $(this).attr('id');
        var id_str_parts = id_str.split('_part_');
        var part_type = id_str_parts[0];
        var part_id = id_str_parts[1];

        var other_part_type = "similar";
        if (part_type == "similar") {
            other_part_type = "suspect";
        }
        var other_part = $('#'+other_part_type+'_part_'+part_id);

        if (event.type == "mouseenter") {
            other_part.addClass("diff_part_hightlight");
            $(this).addClass("diff_part_hightlight");
        } else {
            other_part.removeClass("diff_part_hightlight");
            $(this).removeClass("diff_part_hightlight");
        }
    });
});