<template>
<div>
  <div style="padding-left:10px;padding-right:10px">
    <h1>北京林业大学第十五届青年教师教学基本功比赛（教学反思）</h1>
  </div>
  <div style="text-align:left;padding-left:100px;padding-top:20px;padding-bottom:20px">
    教师姓名：<input v-model="user"/>
  </div>
  <div  style="padding-left:100px;padding-right:100px">
    <textarea style="width:100%; border:solid 1px #d8d8d8; border-radius:3px; font-size:20px; padding:10px;" rows="20" @input="descInput" v-model="desc"></textarea>
    <p class="pay-service-textarea-text">当前您已经输入<span>{{ remnant }}</span>字符</p>
    <Button type="primary" @click="handleSubmit()">提交</Button>
  </div>
</div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'add',
  data () {
    return {
      remnant: 0,
      desc: '',
      maxlength: '',
      user: ''
    }
  },
  methods: {
    descInput () {
      let desc = this.intToChinese(this.desc)
      desc = this.translateString(desc)
      let cnReg = /([\u4e00-\u9fa5])/g
      let mat = desc.match(cnReg)
      var txtVal
      if (mat) {
        txtVal = mat.length
      } else {
        txtVal = 0
      }
      this.remnant = txtVal
    },
    handleSubmit () {
      var name = this.user
      var desc = this.desc
      axios.post('/api/add', { name: name, text: desc }).then(({ data }) => {
        this.desc = ''
        this.maxlength = true
      })
    },
    translateString (str) {
      const Translator = require('../assets/translator')
      let translator = new Translator()

      // config the translator
      translator.config = {
        from: 'EN', // zh-CHS(中文) || ja(日语) || EN(英文) || fr(法语) ...
        to: 'zh-CHS',
        appKey: '52e18bd7cbb763a3', // https://ai.youdao.com 在有道云上进行注册
        secretKey: '2fgcTN25x3B5y9RKpM6tghV05cwl5MF2'
      }
      let resultStr = translator.translate(str)
      console.log(resultStr)
      return resultStr
    },
    intToChinese (str) {
      str = str + ''
      var len = str.length - 1
      // eslint-disable-next-line
      var idxs = ['', '十', '百', '千', '万', '十', '百', '千', '亿', '十', '百', '千', '万', '十', '百', '千', '亿'];
      var num = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
      return str.replace(/([1-9]|0+)/g, function ($, $1, idx, full) {
        var pos = 0
        // eslint-disable-next-line
        if ($1[0] != '0') {
          pos = len - idx
          // eslint-disable-next-line
          if (idx == 0 && $1[0] == 1 && idxs[len - idx] == '十') {
            return idxs[len - idx]
          }
          return num[$1[0]] + idxs[len - idx]
        } else {
          var left = len - idx
          var right = len - idx + $1.length
          if (Math.floor(right / 4) - Math.floor(left / 4) > 0) {
            pos = left - left % 4
          }
          if (pos) {
            return idxs[pos] + num[$1[0]]
          } else if (idx + $1.length >= len) {
            return ''
          } else {
            return num[$1[0]]
          }
        }
      })
    }
  }
}
</script>
