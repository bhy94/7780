<template>
  <footer class="app_footer">

    <!-- Other -->
    <div class="extra">
      <div class="container">

        <!-- Copyright Information -->
        
        <div style="color:#999;width:100%;display:flex;justify-content:center;padding-top:30px">
          <table class="mytable">
            <tr>
              <th>Responsibility</th>
              <th>Name</th>
              <th>StudentID</th>
            </tr>
            <tr>
              <td>Scrum Master</td>
              <td>Yiming Hong</td>
              <td>23462264</td>
            </tr>
            <tr>
              <td>Scrum Master</td>
              <td>HAOLIN LIU</td>
              <td>23439327</td>
            </tr>
            <tr>
              <td>Developer</td>
              <td>Fuquan Wen</td>
              <td>23462426</td>
            </tr>
            <tr>
              <td>Developer</td>
              <td>HONGYI BIAN</td>
              <td>23458836</td>
            </tr>
          </table>
        </div>
        <div class="copyright">

          <p>CopyRight © GROUP29-7780</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped lang='scss'>
.mytable {
  th {
    padding: 10px;
    text-align: center;
    background-color: #f5f5f5;
    border-radius: 10px;
  };
  td {
    padding: 10px;
    text-align: center;
  };
}

.app_footer {
  overflow: hidden;
  background-color: #f5f5f5;
  padding-top: 20px;

  .contact {
    background: #fff;

    .container {
      padding: 60px 0 40px 25px;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    dl {
      height: 190px;
      text-align: center;
      padding: 0 72px;
      border-right: 1px solid #f2f2f2;
      color: #999;

      &:first-child {
        padding-left: 0;
      }

      &:last-child {
        border-right: none;
        padding-right: 0;
      }
    }

    dt {
      line-height: 1;
      font-size: 18px;
    }

    dd {
      margin: 36px 12px 0 0;
      float: left;
      width: 92px;
      height: 92px;
      padding-top: 10px;
      border: 1px solid #ededed;

      .iconfont {
        font-size: 36px;
        display: block;
        color: #666;
      }

      &:hover {
        .iconfont {
          color: $xtxColor;
        }
      }

      &:last-child {
        margin-right: 0;
      }
    }

    .qrcode {
      width: 92px;
      height: 92px;
      padding: 7px;
      border: 1px solid #ededed;
    }

    .download {
      padding-top: 5px;
      font-size: 14px;
      width: auto;
      height: auto;
      border: none;

      span {
        display: block;
      }

      a {
        display: block;
        line-height: 1;
        padding: 10px 25px;
        margin-top: 5px;
        color: #fff;
        border-radius: 2px;
        background-color: $xtxColor;
      }
    }

    .hotline {
      padding-top: 20px;
      font-size: 22px;
      color: #666;
      width: auto;
      height: auto;
      border: none;

      small {
        display: block;
        font-size: 15px;
        color: #999;
      }
    }
  }

  .extra {
    background-color: #333;
  }

  .slogan {
    height: 178px;
    line-height: 58px;
    padding: 60px 100px;
    border-bottom: 1px solid #434343;
    display: flex;
    justify-content: space-between;

    a {
      height: 58px;
      line-height: 58px;
      color: #fff;
      font-size: 28px;

      i {
        font-size: 50px;
        vertical-align: middle;
        margin-right: 10px;
        font-weight: 100;
      }

      span {
        vertical-align: middle;
        text-shadow: 0 0 1px #333;
      }
    }
  }

  .copyright {
    height: 170px;
    padding-top: 40px;
    text-align: center;
    color: #999;
    font-size: 15px;

    p {
      line-height: 1;
      margin-bottom: 20px;
    }

    a {
      color: #999;
      line-height: 1;
      padding: 0 10px;
      border-right: 1px solid #999;

      &:last-child {
        border-right: none;
      }
    }
  }
}
</style>
