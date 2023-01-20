// Adapted from Whitelist API https://juejin.cn/post/6844903930040680462
const xssFilter = ()=>{
  if(!html) return '';
  const xss = require('xss');
  const ret = xss(html,{
      whiteList:{
          img:['src'],
          a:['href'],
          font:['color','size'],
      },
      onIgnoreTag(){
          return '';
      }
  });
  return ret;
}