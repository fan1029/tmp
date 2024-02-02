import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/getData",
    method: "get",
    response: request => {
      const { currentPage, pageSize } = request.query;
      const data = [];
      for (let i = 0; i < 100; i++) {
        data.push({
          url: "www.jd.com",
          ip: "2.2.2.2",
          tag: "M123",
          domain: "jd.com"
        });
      }
      const start = (currentPage - 1) * pageSize;
      const end = start + parseInt(pageSize);
      const pageData = data.slice(start, end);
      return {
        success: true,
        length: data.length,
        data: pageData,
        start: start,
        end: end
      };
    }
  }
] as MockMethod[];
