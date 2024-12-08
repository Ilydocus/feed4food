import React, { useState } from 'react';

const ProduceSubmissionForm = () => {
  const [formData, setFormData] = useState({
    produceName: '',
    quantity: '',
    price: '',
    description: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Produce Submitted:', formData);
    // Add logic to send data to the backend (e.g., via a REST API)
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Submit Farm Produce</h2>
      <label>
        Produce Name:
        <input type="text" name="produceName" value={formData.produceName} onChange={handleChange} required />
      </label>
      <label>
        Quantity (e.g., kg or units):
        <input type="number" name="quantity" value={formData.quantity} onChange={handleChange} required />
      </label>
      <label>
        Price (per unit):
        <input type="number" name="price" value={formData.price} onChange={handleChange} required />
      </label>
      <label>
        Description:
        <textarea name="description" value={formData.description} onChange={handleChange} />
      </label>
      <button type="submit">Submit Produce</button>
    </form>
  );
};

export default ProduceSubmissionForm;
