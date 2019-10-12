$(function () {
    // 根据后台返回json数据，初始化整个菜单树
    // 第一步，请求后台菜单数据

    $.ajax({
        type: 'GET',
        url: '/app_c_rbac/get_menu_data/?get_type=system',
        success: function (response_data) {

            // node = response_data.data.node;
            // console.log(node);
            // 第二步，初始化菜单树
            $("#jstree_div").jstree({
                'core' : {
                    'themes': {
                        'dots': true
                    },
                    // 使用JSON数据显示菜单树
                    // 'data' : [
                    //     {
                    //         "text" : "Root node",
                    //         "icon" : "glyphicon glyphicon-tags",
                    //         "children" : [
                    //             {
                    //                 "text" : "Child node 1",
                    //                 "icon" : "glyphicon glyphicon-tag"
                    //             },
                    //             { "text" : "Child node 2" }
                    //         ]
                    //     }
                    // ]
                    'data': response_data.data.node
                },
                "checkbox" : {
                    "keep_selected_style" : false
                },
                "plugins" : [ "checkbox" ]
            });

        }
    });

    $('#menu_commit').click(function () {
        var ref = $('#jstree_div').jstree(true);//获取整个树节点
        // var sel = ref.get_selected(false);//获得所有选中节点，返回值为数组
        var check = ref.get_checked(true)
        console.log(check)

    });



});
