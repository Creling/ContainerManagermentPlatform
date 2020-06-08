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
                >部署服务</el-button>
                <el-button
                    type="primary"
                    icon="el-icon-edit"
                    class="handle-add mr10"
                    @click="handleAdvanceDelete"
                >高级删除</el-button>
                <el-button
                    type="primary"
                    icon="el-icon-edit"
                    class="handle-add mr10"
                    @click="handleAdvanceSelect"
                >高级筛选</el-button>
            </div>

            <el-table
                :data="tableData.slice((pagination.currentPage-1)*pagination.pageSize, pagination.currentPage*pagination.pageSize)"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
                @selection-change="handleSelectionChange"
                :span-method="objectSpanMethod"
            >
                <el-table-column prop="ServiceName" label="服务名称"></el-table-column>
                <el-table-column prop="Describe" label="描述"></el-table-column>
                <el-table-column prop="ContainerName" label="容器名称"></el-table-column>
                <el-table-column prop="DatacenterName" label="数据中心"></el-table-column>
                <el-table-column prop="CityName" label="城市"></el-table-column>
                <el-table-column prop="NationName" label="国家"></el-table-column>
                <el-table-column prop="StartTime" label="启动时间"></el-table-column>
                <el-table-column prop="ServiceComment" label="备注"></el-table-column>
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
        <el-dialog :title="action + '服务'" :visible.sync="dialogFormVisible" width="40%">
            <el-form :model="form" :label-position="'left'">
                <el-form-item label="服务名称" :label-width="formLabelWidth">
                    <el-select v-model="ServiceName" placeholder="请选择">
                        <el-option
                            v-for="item in ServiceNameOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="容器名称" :label-width="formLabelWidth">
                    <el-select v-model="ContainerName" placeholder="请选择">
                        <el-option
                            v-for="item in ContainerNameOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="启动时间" :label-width="formLabelWidth">
                    <el-input v-model="form.StartTime" autocomplete="off" size="small"></el-input>
                </el-form-item>
                <el-form-item label="备注" :label-width="formLabelWidth">
                    <el-input v-model="form.Comment" autocomplete="off" size="small"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible=false">取 消</el-button>
                <el-button type="primary" @click="submitHost()">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog :title="action" :visible.sync="advanceVisable" width="40%">
            <el-form :model="advance" :label-position="'left'">
                <el-form-item label="属性" :label-width="formLabelWidth">
                    <el-input v-model="advance.Char" autocomplete="off" size="small"></el-input>
                </el-form-item>
                <el-form-item label="属性值" :label-width="formLabelWidth">
                    <el-input v-model="advance.Value" autocomplete="off" size="small"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible=false">取 消</el-button>
                <el-button type="primary" @click="submitAdvanceInfo()">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>
<script>
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
                pageSize: 10,
                pageTotal: 2
            },
            tableData: [],
            multipleSelection: [],
            delList: [],
            ServiceName: '',
            ContainerName: '',
            ContainerNameOptions: [],
            ServiceNameOptions: [],
            idx: -1,
            id: -1,
            dialogFormVisible: false,
            form: {},
            login: {
                username: '',
                password: ''
            },
            formLabelWidth: '80px',
            editform: '',
            spanArr: [],
            position: 0,
            advance: {},
            advanceVisable: false,
        };
    },
    created() {
        this.getData();
    },
    methods: {
        getData() {
            this.tableData = [];
            request.get('/api/servicecontainer').then(
                res => {
                    console.log(res);
                    this.tableData = res.ContainerService;
                    this.tableData.forEach((item, index) => {
                        console.log('forEach');
                        if (index === 0) {
                            this.spanArr.push(1);
                            this.position = 0;
                        } else {
                            if (this.tableData[index].ServiceName === this.tableData[index - 1].ServiceName) {
                                this.spanArr[this.position] += 1;
                                this.spanArr.push(0);
                            } else {
                                this.spanArr.push(1);
                                this.position = index;
                            }
                        }
                    });
                },
                error => {
                    console.log(error);
                }
            );
        },
        getOption() {
            request.get('/api/service').then(
                res => {
                    console.log(res.Service);
                    this.ServiceNameOptions = [];
                    for (let i = 0; i < res.Service.length; i++) {
                        this.ServiceNameOptions.push({ label: res.Service[i].ServiceName, value: res.Service[i].ServiceName });
                    }
                },
                error => {
                    console.log(error);
                }
            );

            request.get('/api/container').then(
                res => {
                    console.log(res.Container);
                    this.ContainerNameOptions = [];
                    for (let i = 0; i < res.Container.length; i++) {
                        this.ContainerNameOptions.push({ label: res.Container[i].ContainerName, value: res.Container[i].ContainerName });
                    }
                },
                error => {
                    console.log(error);
                }
            );
        },
        // 登录
        submitLogin() {
            request.post('//39.96.212.204:8081/api/login', { user: this.login.username, password: this.login.password }).then(
                res => {
                    this.$message.success('登录成功');
                    localStorage.setItem('ms_username', this.login.username);
                    this.loginVisible = false;
                    this.getData();
                },
                err => {
                    if (err === 403) {
                        this.$message.error('账户名或密码错误');
                        this.login.username = '';
                        this.login.password = '';
                    }
                }
            );
        },
        // 删除操作
        handleDelete(index, row) {
            // 二次确认删除
            console.log(row.NationName);
            this.$confirm('确定要删除吗？', '提示', {
                type: 'warning'
            }).then(() => {
                request
                    .delete('/api/servicecontainer', {
                        data: JSON.stringify({ ServiceName: row.ServiceName, ContainerName: row.ContainerName })
                    })
                    .then(res => {
                        console.log(res);
                        this.$message.success('删除成功');
                        this.getData();
                    });
            });
        },
        // 打开ssh连接页面
        handleGo(index, row) {
            let ip = row.server_ip;
            let url = `/ssh/${row.server_ip}/${Date.now().toString(35)}/${row.server_name}`;
            console.log(url);
            this.$router.push(url);
        },
        // 打开sftp连接页面
        handleDocument(index, row) {
            let ip = row.server_ip;
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
            this.action = '编辑';
            this.dialogFormVisible = true;
            this.form = Object.assign({}, row);
        },
        // 分页导航
        handlePageChange(val) {
            this.pagination.currentPage = val;
        },
        // 添加主机
        handleAdd() {
            this.action = '添加';
            this.form = {};
            this.getOption();
            this.dialogFormVisible = true;
        },
        submitHost() {
            request
                .put('/api/servicecontainer', {
                    ContainerName: this.ContainerName,
                    ServiceName: this.ServiceName,
                    StartTime: this.form.StartTime,
                    Comment: this.form.Comment
                })
                .then(
                    res => {
                        console.log(res);
                        this.dialogFormVisible = false;
                        this.$message.success('添加成功');
                        this.getData();
                    },
                    err => {
                        if (err === 403) {
                            this.$message.error('未登录或登录已失效');
                        }
                    }
                );
        },
        objectSpanMethod({ row, column, rowIndex, columnIndex }) {
            if (columnIndex === 0) {
                const _row = this.spanArr[rowIndex];
                const _col = _row > 0 ? 1 : 0;
                return {
                    rowspan: _row,
                    colspan: _col
                };
            }
            if (columnIndex === 1) {
                const _row = this.spanArr[rowIndex];
                const _col = _row > 0 ? 1 : 0;
                return {
                    rowspan: _row,
                    colspan: _col
                };
            }
        },
        submitAdvanceInfo() {
            if ((this.action === "高级删除")) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    request
                        .delete('/api/servicecontainer', { data: JSON.stringify({ Char: this.advance.Char, Value: this.advance.Value }) })
                        .then(res => {
                            this.$message.success('删除成功');
                            this.getData();
                        });
                });
            } else if ((this.action === "高级筛选")) {
                request.get('/api/servicecontainer', { params: { Char: this.advance.Char, Value: this.advance.Value } }).then(res => {
                    this.$message.success('筛选成功');
                    this.advanceVisable = false
                    this.tableData = res.ContainerService
                });
            }
        },
        handleAdvanceDelete() {
            this.action = '高级删除';
            this.advanceVisable = true;
        },
        handleAdvanceSelect() {
            this.action = '高级筛选';
            this.advanceVisable = true;
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
