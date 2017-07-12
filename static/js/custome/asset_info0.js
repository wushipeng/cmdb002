/**
 * Created by Administrator on 2017/7/9 0009.
 */
  var csrftoken = Cookies.get("csrftoken");

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                // settings 会获取到ajax里面的所有配置

                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);

                }
            }
        });


        function deleteasset(obj) {
            var d = dialog({

                content: '你确定要删除吗?',
                okValue: '确定',
                ok: function () {
                    var url_id = $(obj).attr("url");
                    $.ajax({
                        url: '/asset_delete/' + url_id,
                        dataType: 'JSON',
                        traditional: true,
                        type: 'POST',
                        success: function (data) {
                            var info = data["info"];
                            var count = $("th").size();
                            $(obj).parent()
                                    .parent().parent().text("")
                                    .append("<td colspan=" + count + " style='text-align:center;color:red'>" + info + "</td>")
                        }
                    });

                },
                cancelValue: '取消',
                cancel: function () {
                }
            });
            d.show();
        }
        ;

        var store = window.localStorage;
        $('#find').click(function () {
            store.setItem('ip', $("input[name='ip']").val());
            store.setItem('hostname', $("input[name='hostname']").val())
            store.setItem('indistinct', '')
        });
        $('#search').click(function () {
            store.setItem('indistinct', $("input[name='indistinct']").val())
            store.setItem('ip', '');
            store.setItem('hostname', '')
        });
        $('#clear_ip').click(function () {
            $("input[name='ip']").val("");
            $('#clear_ip').attr("hidden", "hidden")
        });
        $('#clear_hostname').click(function () {
            $("input[name='hostname']").val("");
            $('#clear_hostname').attr("hidden", "hidden")
        });
        $('#clear_search').click(function () {
            $("input[name='indistinct']").val("");
            $('#clear_search').attr("hidden", "hidden")
        });
        $(function () {
            var eee = $("span[name='ip']").text();
            // console.log(store.getItem('hostname'));
            $("input[name='ip']").val(store.getItem('ip'));
            $("input[name='hostname']").val(store.getItem('hostname'));
            $("input[name='indistinct']").val(store.getItem('indistinct'));
            // console.log(store.getItem('indistinct'));
            if ($("input[name='ip']").val().length > 0) {
                $('#clear_ip').removeAttr("hidden");
            }
            if ($("input[name='hostname']").val().length > 0) {
                console.log("21e123")
                $('#clear_hostname').removeAttr("hidden")
            }
            else if ($("input[name='indistinct']").val().length > 0) {
                $('#clear_search').removeAttr("hidden");
            }
            console.log($("input[name='hostname']").val().length)
        });
        function change_ip() {
            $('#clear_ip').removeAttr("hidden")
            if ($("input[name='ip']").val().length == 0) {
                $('#clear_ip').attr("hidden", "hidden")
            }
        }
        ;

        function change_hostname() {
            $('#clear_hostname').removeAttr("hidden");
            if ($("input[name='hostname']").val().length == 0) {
                $('#clear_hostname').attr("hidden", "hidden")
            }
        };
        function change_search() {
            $('#clear_search').removeAttr("hidden");
            if ($("input[name='indistinct']").val().length == 0) {
                $('#clear_search').attr("hidden", "hidden")
            }
        };