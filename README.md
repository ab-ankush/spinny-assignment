
# Spinny Assignment

This is the code for the Assignment given to me.


## Authentication
To authenticate, Provide the **username** and **password**, in the Basic Authentication in the **`Auth Section`**

There are 3 users currently with username - **`root`**, **`root2`** and **`test`**, all having the same password **`root`**

**root** and **root2** have the staff settings enabled while as **test** does not.





## API Reference

#### Create a new Box

```http
  Post /api/create
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `length` | `string` | **Required**. Length of the box |
| `breadth` | `string` | **Required**. breadth of the box |
| `height` | `string` | **Required**. height of the box | 


#### Update a box

```http
  PATCH /api/update/${id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `length` | `string` | **Optional**. Length of the box |
| `breadth` | `string` | **Optional**. breadth of the box |
| `height` | `string` | **Optional**. height of the box |



#### Get all Boxes

```http
  GET /api/list/
```
**We can use query strings after the url to add optional parametere**

These parameters are

    1.length_more_than or length_less_than
    2.breadth_more_than or breadth_less_than
    3.height_more_than or height_less_than
    4.area_more_than or area_less_than
    5.volume_more_than or volume_less_than
    6.username
    7.created_before or created_after

#### List individual Boxes

```http
  GET /api/list-user-boxes
```
**We can use query strings after the url to add optional parametere**

These parameters are

    1.length_more_than or length_less_than
    2.breadth_more_than or breadth_less_than
    3.height_more_than or height_less_than
    4.area_more_than or area_less_than
    5.volume_more_than or volume_less_than

#### Delete a box with given id

```http
  DELEYE /api/delete/${id}
```


