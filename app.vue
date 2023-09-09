<template>
  <div class="container">
    <h1>Students:</h1>

    <!-- Add Student Form -->
    <div class="form-container">
      <h2>Add Student:</h2>
      <form @submit.prevent="addStudent" class="student-form">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" v-model="studentData.name" required>
        </div>

        <div class="form-group">
          <label for="age">Age:</label>
          <input type="number" v-model="studentData.age" required>
        </div>
        
        <div class="form-group">
          <label for="mark">Mark:</label>
          <input type="number" v-model="studentData.mark" required>
        </div>
        
        <button type="submit" class="submit-button">Submit</button>
      </form>
      <button @click="updateStudent" class="update-button">Update</button>
    </div>

    <!-- List of Students -->
    <h2>Student List</h2>
    <ul class="student-list">
      <li v-for="student in students" :key="student.id" class="student-item">
        {{ student.name }} - Age: {{ student.age }} - Mark: {{ student.mark }}
        <button @click="deleteStudent(student.student_id)" class="delete-button">Delete</button>
        <button @click="reloadStudent(student.student_id)" class="reload-button">Update</button>
      </li>
    </ul>
  </div>
</template>

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1, h2 {
  text-align: center;
}

.form-container {
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 8px;
}

.student-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 10px;
}

label {
  font-weight: bold;
}

input[type="text"],
input[type="number"] {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.submit-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
}

.update-button {
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.student-list {
  list-style: none;
  padding: 0;
}

.student-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.delete-button {
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.reload-button {
  background-color: #ffc107;
  color: #000;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}
</style>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const studentData = ref({ name: "", age: 0, mark: 0 ,id:0});
    const students = ref([]);
    async function updateStudent(){
      try{
      const response = await axios.put(`http://127.0.0.1:5000/api/students/${studentData.value.id}`,studentData.value);
      if (response.status === 200) {
          console.log('Student updated successfully');
          getStudents()

        } else {
          console.error('Failed to update student');
        }
      } catch (error) {
        console.error('Error updating student:', error);
      }

    }
    
    async function addStudent() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/students', studentData.value);
        const response2 = await axios.get('http://127.0.0.1:5000/api/students');
        if (response.status === 200) {
          students.value = response2.data.students;
          studentData.value = { name: '', age: 0, mark: 0 };
        } else {
          console.error('Failed to add student');
        }
      } catch (error) {
        console.error('Error adding student:', error);
      }
    }

    async function getStudents() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/students');
        if (response.status === 200) {
          students.value = response.data.students;
        } else {
          console.error('Failed to fetch students');
        }
      } catch (error) {
        console.error('Error fetching students:', error);
      }
    }
    async function deleteStudent(studentId) {
      try {
        const response = await axios.delete(`http://127.0.0.1:5000/api/students/${studentId}`);
        if (response.status === 200) {
          console.log('Student deleted successfully');
          getStudents();
        } else {
          console.error('Failed to delete student');
        }
      } catch (error) {
        console.error('Error deleting student:', error);
      }
    }



    
    async function reloadStudent(studentId) {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/students/${studentId}`);
    studentData.value = { name: response.data.student[1], age: response.data.student[2], mark: response.data.student[3],id:response.data.student[0]};
    if (response.status === 200) {
      console.log('Student reloaded successfully');
      getStudents();
    } else {
      console.error('Failed to reload student');
    }
  } catch (error) {
    console.error('Error reloading student:', error);
  }
}
    onMounted(() => {
      getStudents();
    });

    return {
      studentData,
      students,
      addStudent,
      deleteStudent,reloadStudent
      ,updateStudent
    };
  },
};
</script>
