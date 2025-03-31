## GraphQL Schema

```graphql
type User {
	id: ID!
	username: String
	name: String
	password: String
	first_login: String!
	project_closed_count: Int!
	project_open_count: Int!
	projects_aborted_count: Int!
	avatar_url: String
	projects: [String]
	notifications: [String]
	email: String
	otp: Boolean
	code_otp: String
}

type Tasks {
	id: ID!
	name: String
	description: String
	created: String
	who_create: String
	status: String
	type: String
	assignee: String
	rating: Int
	tag: String
	priority: String
	completed_date: String
}

type Project {
	id: ID!
	name: String
	description: String
	created: String
	who_create: WHOCREATEPROJECT!
	status: String
	tasks: [Tasks]
	collaborators: [Collaborators]
	history: [String]
}

type Token {
	data: String!
}

type StatusMessageProject {
	status: String!
}

type Collaborators {
	id: ID!
	username: String
}

type WHOCREATEPROJECT {
	id: ID!
	username: String!
}
```

---

# Available REST Routes, Queries, and Mutations

## **REST Routes**

### 1. **`GET /download/csv/<project_id>/<token>`**

- **Description**: Generates and returns a CSV report for a specific project.
- **Parameters**:
  - `project_id`: Project ID.
  - `token`: User authentication token.
- **Return**: CSV file containing the project data.

### 2. **`GET /download/pdf/<project_id>/<token>`**

- **Description**: Generates and returns a PDF report for a specific project.
- **Parameters**:
  - `project_id`: Project ID.
  - `token`: User authentication token.
- **Return**: PDF file containing the project data.

---

## **Available Queries**

### **Users**

1. **`users`**

   - **Description**: Returns a list of all users.
   - **Resolver**: `listUsers_resolver`
   - **Return**: List of `User` objects.

2. **`user(id: ID!)`**

   - **Description**: Returns details of a specific user.
   - **Resolver**: `getUser_resolver`
   - **Arguments**:
     - `id`: User ID.
   - **Return**: `User` object.

3. **`userCount`**
   - **Description**: Returns the total number of users.
   - **Resolver**: `usersCount_resolver`
   - **Return**: Total number of users.

### **Projects**

4. **`projects`**

   - **Description**: Returns a list of all projects.
   - **Resolver**: `listProjects_resolver`
   - **Return**: List of `Project` objects.

5. **`project(id: ID!)`**

   - **Description**: Returns details of a specific project.
   - **Resolver**: `getProjects_resolver`
   - **Arguments**:
     - `id`: Project ID.
   - **Return**: `Project` object.

6. **`projectsCount`**
   - **Description**: Returns the total number of projects.
   - **Resolver**: `projectsCount_resolver`
   - **Return**: Total number of projects.

---

## **Available Mutations**

### **Users**

1. **`createUser(name: String!, username: String!, password: String!)`**

   - **Description**: Creates a new user.
   - **Resolver**: `createUser`
   - **Arguments**:
     - `name`: User's name.
     - `username`: Username.
     - `password`: User's password.
   - **Return**: `User` object.

2. **`deleteUser`**

   - **Description**: Deletes the authenticated user.
   - **Resolver**: `deleteUser`
   - **Return**: Deleted `User` object.

3. **`login(username: String!, password: String!)`**

   - **Description**: Logs in a user.
   - **Resolver**: `userLogin`
   - **Arguments**:
     - `username`: Username.
     - `password`: User's password.
   - **Return**: `Token` object.

4. **`clearNotifications`**

   - **Description**: Clears all notifications of the authenticated user.
   - **Resolver**: `cleanNotificationsUser`
   - **Return**: Status message.

5. **`updateAvatar(avatarUrl: String!)`**

   - **Description**: Updates the avatar of the authenticated user.
   - **Resolver**: `changeAvatarUrlUser`
   - **Arguments**:
     - `avatarUrl`: URL of the new avatar.
   - **Return**: Status message.

6. **`changeEmailUser(email: String!)`**

   - **Description**: Updates the email of the authenticated user.
   - **Resolver**: `changeEmailUser`
   - **Arguments**:
     - `email`: New email.
   - **Return**: Status message.

7. **`turnOTPUser`**

   - **Description**: Enables or disables OTP authentication for the authenticated user.
   - **Resolver**: `turnOTPUser`
   - **Return**: Status message.

8. **`verifyOtp(otp: String!)`**
   - **Description**: Verifies the user's OTP code.
   - **Resolver**: `verifyOtp`
   - **Arguments**:
     - `otp`: OTP code.
   - **Return**: `Token` object.

### **Projects**

9. **`createProject(nameProject: String!, descriptionProject: String!)`**

   - **Description**: Creates a new project.
   - **Resolver**: `createProject`
   - **Arguments**:
     - `nameProject`: Project name.
     - `descriptionProject`: Project description.
   - **Return**: `Project` object.

10. **`deleteProject(idProject: String!)`**

    - **Description**: Deletes a project.
    - **Resolver**: `deleteProject`
    - **Arguments**:
      - `idProject`: Project ID.
    - **Return**: Status message.

11. **`addCollaborator(idProject: String!, idCollaborator: String!)`**

    - **Description**: Adds a collaborator to a project.
    - **Resolver**: `addCollaboratorProject`
    - **Arguments**:
      - `idProject`: Project ID.
      - `idCollaborator`: Collaborator ID.
    - **Return**: Status message.

12. **`removeCollaborator(idProject: String!, idCollaborator: String!)`**

    - **Description**: Removes a collaborator from a project.
    - **Resolver**: `removeCollaboratorProject`
    - **Arguments**:
      - `idProject`: Project ID.
      - `idCollaborator`: Collaborator ID.
    - **Return**: Status message.

13. **`closeProject(idProject: String!)`**
    - **Description**: Closes a project, changing its status to "closed".
    - **Resolver**: `closeStatusProject`
    - **Arguments**:
      - `idProject`: Project ID.
    - **Return**: Status message.
