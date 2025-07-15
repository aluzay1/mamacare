# MamaCare Custom FHIR Extensions

This document describes the custom FHIR extensions used in the MamaCare system to support maternal care and pregnancy-related data that are not covered by standard FHIR resources.

## Extension Base URL
All custom extensions use the base URL: `http://mamacare.com/fhir/StructureDefinition/`

## Patient Extensions

### 1. Blood Type Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-bloodType`
- **Type**: CodeableConcept
- **Cardinality**: 0..1
- **Description**: Patient's blood type (A+, A-, B+, B-, O+, O-, AB+, AB-)
- **Value Set**: Standard blood type codes

### 2. Nationality Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-nationality`
- **Type**: CodeableConcept
- **Cardinality**: 0..1
- **Description**: Patient's nationality
- **Value Set**: ISO 3166-1 alpha-2 country codes

### 3. Pregnancy Status Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-pregnancyStatus`
- **Type**: CodeableConcept
- **Cardinality**: 0..1
- **Description**: Current pregnancy status
- **Value Set**: 
  - `not_pregnant` - Not pregnant
  - `pregnant` - Currently pregnant
  - `postpartum` - Postpartum period

### 4. Last Menstrual Period Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-lmpDate`
- **Type**: Date
- **Cardinality**: 0..1
- **Description**: Date of last menstrual period (LMP)

### 5. Estimated Due Date Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-dueDate`
- **Type**: Date
- **Cardinality**: 0..1
- **Description**: Estimated due date calculated from LMP

### 6. Gestational Age Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-gestationalAge`
- **Type**: Integer
- **Cardinality**: 0..1
- **Description**: Gestational age in weeks

### 7. Multiple Pregnancy Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-multiplePregnancy`
- **Type**: CodeableConcept
- **Cardinality**: 0..1
- **Description**: Type of multiple pregnancy
- **Value Set**:
  - `no` - Single pregnancy
  - `twins` - Twin pregnancy
  - `triplets` - Triplet or higher order pregnancy

### 8. Pregnancy Risk Level Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-pregnancyRiskLevel`
- **Type**: CodeableConcept
- **Cardinality**: 0..1
- **Description**: Pregnancy risk assessment level
- **Value Set**:
  - `low` - Low risk pregnancy
  - `medium` - Medium risk pregnancy
  - `high` - High risk pregnancy

### 9. Previous Pregnancies Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-previousPregnancies`
- **Type**: Integer
- **Cardinality**: 0..1
- **Description**: Number of previous pregnancies

### 10. Prenatal Vitamins Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-prenatalVitamins`
- **Type**: String
- **Cardinality**: 0..1
- **Description**: List of prenatal vitamins and supplements being taken

### 11. Emergency Hospital Extension
- **URL**: `http://mamacare.com/fhir/StructureDefinition/patient-emergencyHospital`
- **Type**: String
- **Cardinality**: 0..1
- **Description**: Preferred emergency hospital for pregnancy care

## Related FHIR Resources

### Observation Resources
The following observations are created for pregnancy-related measurements:

1. **Blood Pressure Observation**
   - **Code**: LOINC 55284-4 (Blood pressure panel)
   - **Value**: Quantity with systolic/diastolic values

2. **Hemoglobin Observation**
   - **Code**: LOINC 718-7 (Hemoglobin)
   - **Value**: Quantity in g/dL

3. **Blood Sugar Observation**
   - **Code**: LOINC 2339-0 (Glucose)
   - **Value**: Quantity in mg/dL

4. **Weight Observation**
   - **Code**: LOINC 29463-7 (Body weight)
   - **Value**: Quantity in kg

### Condition Resources
1. **Pregnancy Complications Condition**
   - **Code**: SNOMED CT codes for pregnancy complications
   - **Clinical Status**: Active
   - **Verification Status**: Confirmed

2. **Risk Factors Condition**
   - **Code**: SNOMED CT codes for pregnancy risk factors
   - **Clinical Status**: Active
   - **Verification Status**: Confirmed

### AllergyIntolerance Resources
- **Type**: Allergy
- **Category**: Medication, Food, Environment
- **Criticality**: Low, High
- **Reaction**: Manifestation codes

### MedicationStatement Resources
- **Status**: Active, Completed, Entered-in-error
- **Medication**: CodeableConcept with medication codes
- **Effective Period**: Date range
- **Dosage**: Structured dosage information

### CarePlan Resources
- **Status**: Active, Completed, Entered-in-error
- **Intent**: Plan
- **Category**: Pregnancy care plan
- **Title**: Birth plan
- **Description**: Detailed birth plan information

## Implementation Notes

1. **Extensions**: All custom extensions are added to the Patient resource using the `extension` field.

2. **Resource References**: Related resources (Observation, Condition, etc.) reference the Patient resource using `Patient/{patient_id}`.

3. **Coding Systems**: 
   - LOINC for laboratory and clinical observations
   - SNOMED CT for conditions and clinical findings
   - ICD-10 for diagnoses where applicable

4. **Validation**: All extensions include proper validation and error handling.

5. **Versioning**: Extensions are versioned and documented for backward compatibility.

## Example Usage

```json
{
  "resourceType": "Patient",
  "id": "patient-123",
  "extension": [
    {
      "url": "http://mamacare.com/fhir/StructureDefinition/patient-bloodType",
      "valueCodeableConcept": {
        "coding": [
          {
            "system": "http://mamacare.com/fhir/CodeSystem/blood-type",
            "code": "O+",
            "display": "O Positive"
          }
        ]
      }
    },
    {
      "url": "http://mamacare.com/fhir/StructureDefinition/patient-pregnancyStatus",
      "valueCodeableConcept": {
        "coding": [
          {
            "system": "http://mamacare.com/fhir/CodeSystem/pregnancy-status",
            "code": "pregnant",
            "display": "Currently Pregnant"
          }
        ]
      }
    }
  ],
  "name": [
    {
      "use": "official",
      "family": "Doe",
      "given": ["Jane", "Marie"]
    }
  ],
  "gender": "female",
  "birthDate": "1990-01-01"
}
```

## Future Enhancements

1. **Standard Extensions**: Where possible, replace custom extensions with standard FHIR extensions as they become available.

2. **Value Set Expansion**: Expand value sets to include more granular codes for better interoperability.

3. **Profile Development**: Create FHIR profiles to standardize the use of these extensions across implementations.

4. **Terminology Server**: Integrate with a terminology server for dynamic code validation and expansion. 