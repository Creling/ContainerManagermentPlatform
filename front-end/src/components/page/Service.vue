<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 容器列表
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button
                    type="primary"
                    icon="el-icon-delete"
                    class="handle-del mr10"
                    @click="getData"
                >刷新数据</el-button>
                <el-button
                    type="primary"
                    icon="el-icon-edit"
                    class="handle-add mr10"
                    @click="handleAdd"
                >添加容器</el-button>
            </div>

            <el-table
                :data="tableData.slice((pagination.currentPage-1)*pagination.pageSize, pagination.currentPage*pagination.pageSize)"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
                @selection-change="handleSelectionChange"
            >
                <el-table-column prop="id" label="ID" v-if='false' ></el-table-column>
                <el-table-column type="index"></el-table-column>
                <el-table-column prop="ServiceName" label="服务名称"></el-table-column>
                <el-table-column prop="Describe" label="描述"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    layout="total, prev, pager, next"
                    :current-page="pagination.currentPage"
                    :page-size="pagination.pageSize"
                    :total="pagination.pageTotal"
                    @current-change="handlePageChange"
                ></el-pagination>
            </div>
        </div>
        <el-dialog :title='action + "服务"' :visible.sync="dialogFormVisible" width='40%'>
            <el-form :model="form" :label-position="'left'">
                <el-form-item label="服务名称" :label-width="formLabelWidth">
                <el-input v-model="form.ServiceName" autocomplete="off" size="small"></el-input>
                </el-form-item>
                <el-form-item label="服务描述" :label-width="formLabelWidth">
                <el-input v-model="form.Describe" autocomplete="off" size="small"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible=false">取 消</el-button>
                <el-button type="primary" @click="submitHost()">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>
<script>
import { fetchData } from '../../api/index';
import request from '@/utils/request';
export default {
    name: 'basetable',
    data() {
        return {
            editVisible: false,
            loginVisible: false,
            action: '',
            pagination: {
                currentPage: 1,
                pageSize: 5,
                pageTotal: 0,
            },
            tableData: [],
            multipleSelection: [],
            delList: [],
            DatacenterName: '',
            ProviderName: '',
            DatacenterNameOptions: [],
            ProviderNameOptions: [],
            idx: -1,
            id: -1,
            dialogFormVisible: false,
            form: {},
            login: {
                username: '',
                password: '',
            },
            formLabelWidth: '80px',
            editform: '',
        };
    },
    created() {
        this.getData();
    },
    methods: {
        getData() {
            request.get('/api/service').then(res => {
                console.log(res);
                this.tableData = res.Service
            }, error => {
                console.log(error);
            });
        },
        getOption() {
            request.get('/api/datacenter').then(res => {
                console.log(res.Datacenter);
                this.DatacenterNameOptions = []
                for (let i = 0; i < res.Datacenter.length; i++) {
                    this.DatacenterNameOptions.push({'label': res.Datacenter[i].DatacenterName, 'value': res.Datacenter[i].DatacenterName})
                }
            }, error => {
                console.log(error);
            });

            request.get('/api/provider').then(res => {
                console.log(res.Provider);
                this.ProviderNameOptions = []
                for (let i = 0; i < res.Provider.length; i++) {
                    this.ProviderNameOptions.push({'label': res.Provider[i].ProviderName, 'value': res.Provider[i].ProviderName})
                }
            }, error => {
                console.log(error);
            });            
        },
        // 登录
        submitLogin() {
            request.post('//39.96.212.204:8081/api/login',
                            {'user': this.login.username, 'password': this.login.password},
            ).then (res => {
                this.$message.success('登录成功');
                localStorage.setItem('ms_username', this.login.username);
                this.loginVisible = false;
                this.getData();
            }, err => {                    
                if (err === 403) {
                    this.$message.error("账户名或密码错误");
                    this.login.username = '';
                    this.login.password = '';
                }
            })
        },
        // 删除操作
        handleDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除吗？', '提示', {
                type: 'warning'
            })
            .then(() => {
                request.delete('/api/service',
                                {data: JSON.stringify(
                                    {'ServiceName': row.ServiceName}
                                )}
                                ).then ( res => {
                                    console.log(res)
                                    this.$message.success('删除成功');
                                    this.getData();
                                }, err => {
                                    if (err === 403) {
                                        this.$message.error('未登录或登录已失效');
                                    }else if (err > 500) {
                                        this.$message.error('服务器错误');
                                    }

                                })
            })
        },
        // 打开ssh连接页面
        handleGo(index, row) {
            let ip = row.server_ip
            let url = `/ssh/${row.server_ip}/${Date.now().toString(35)}/${row.server_name}`;
            console.log(url);
            this.$router.push(url);
        },
        // 打开sftp连接页面
        handleDocument(index, row) {
            let ip = row.server_ip
            let url = `/sftp/${row.server_ip}/${row.server_name}`;
            console.log(url);
            this.$router.push(url);           
        },
        // 多选操作
        handleSelectionChange(val) {
            this.multipleSelection = val;
        },
        delAllSelection() {
            const length = this.multipleSelection.length;
            let str = '';
            this.delList = this.delList.concat(this.multipleSelection);
            for (let i = 0; i < length; i++) {
                str += this.multipleSelection[i].name + ' ';
            }
            this.$message.error(`删除了${str}`);
            this.multipleSelection = [];
        },
        // 编辑操作
        handleEdit(index, row) {
            this.action = '编辑'
            this.dialogFormVisible = true
            this.form = Object.assign({}, row)

        },
        // 分页导航
        handlePageChange(val) {
            this.pagination.currentPage = val
        },
        // 添加主机
        handleAdd() {
            this.action = '添加';
            this.dialogFormVisible = true;
            this.form = {};
            this.form.id = -1

        },
        submitHost() {
            request.put('/api/service',
                        {'ServiceName': this.form.ServiceName,
                         'Describe': this.form.Describe
                        }, 
            ).then( res => {
                console.log(res);
                this.dialogFormVisible = false;
                this.$message.success('添加成功');
                this.getData();
            }, err =>{
                if (err === 403) {
                    this.$message.error('未登录或登录已失效');
                }
            });

        },
        testmessage()
        {
            this.$message.success('测试');
        }
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
