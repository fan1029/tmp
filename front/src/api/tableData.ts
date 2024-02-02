import axios from "axios";

export const fetchData = async (currentPage: number, pageSize: number) => {
  try {
    const response = await axios.get("/getData", {
      params: {
        currentPage,
        pageSize
      }
    });
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

// Example usage
// fetchData(1, 10).then(data => {
//   console.log(data);
// });
