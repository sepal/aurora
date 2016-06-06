

            document.getElementById('similar_to_orig').innerHTML = similar_to.content;
            document.getElementById('suspect_orig').innerHTML = suspect.content;


            var diff = JsDiff.diffWords(suspect.content, similar_to.content);

            var similar_to_processed = document.getElementById('similar_to_processed');
            var suspect_processed = document.getElementById('suspect_processed');

            diff.forEach(function(part, i){
                if (!part.removed && !part.added) {
                    // both sides
                    if (part.value.match(/^[\s,\.]*$/)) {
                        similar_to_processed.innerHTML += part.value;
                        suspect_processed.innerHTML += part.value;
                    } else {
                        similar_to_processed.innerHTML += '<span class="diff_part" id="similar_to_part_' + i + '">' + part.value + '</span>';
                        suspect_processed.innerHTML += '<span class="diff_part" id="suspect_part_' + i + '">' + part.value + '</span>';
                    }
                } else if (!part.removed && part.added) {
                    similar_to_processed.innerHTML += part.value;
                } else if (part.removed && !part.added) {
                    suspect_processed.innerHTML += part.value;
                }
            });

            $('#show_suspect_orig').change(function() {
                if (this.checked) {
                    $('#suspect_processed').addClass("text_disabled");
                    $('#suspect_orig').removeClass("text_disabled");
                } else {
                    $('#suspect_processed').removeClass("text_disabled");
                    $('#suspect_orig').addClass("text_disabled");
                }
            });

            $('#show_similar_to_orig').change(function() {
                if (this.checked) {
                    $('#similar_to_processed').addClass("text_disabled");
                    $('#similar_to_orig').removeClass("text_disabled");
                } else {
                    $('#similar_to_processed').removeClass("text_disabled");
                    $('#similar_to_orig').addClass("text_disabled");
                }
            });



            $(".diff_part").on( "mouseenter mouseleave", function(event) {
                var id_str = $(this).attr('id');
                var id_str_parts = id_str.split('_part_');
                var part_type = id_str_parts[0];
                var part_id = id_str_parts[1];

                var other_part_type = "similar_to";
                if (part_type == "similar_to") {
                    other_part_type = "suspect";
                }
                var other_part = $('#'+other_part_type+'_part_'+part_id);

                console.log("part_type: "+part_type+", part_id: "+part_id+", other_part_type: "+other_part_type+" other_part: "+other_part);

                if (event.type == "mouseenter") {
                    other_part.addClass("diff_part_hightlight");
                    $(this).addClass("diff_part_hightlight");
                } else {
                    other_part.removeClass("diff_part_hightlight");
                    $(this).removeClass("diff_part_hightlight");
                }
            });