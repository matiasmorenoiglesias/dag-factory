import pytest
from dagfactory.codegen import generate_task_code, get_operator_import, generate_dag_file

def test_get_operator_import():
    result = get_operator_import("airflow.operators.bash.BashOperator")
    assert result == "from airflow.operators.bash import BashOperator"

def test_get_operator_import_invalid():
    with pytest.raises(ValueError):
        get_operator_import("BashOperator")

def test_generate_task_code():                                                                                                                                                                                                                     
    task_config = {                                                                                                                                                                                                                                
        "operator": "airflow.operators.bash.BashOperator",                                                                                                                                                                                         
        "bash_command": "echo hello",                                                                                                                                                                                                              
    }                                                                                                                                                                                                                                              
    result = generate_task_code("task_a", task_config)                                                                                                                                                                                             
    assert "task_a = BashOperator(" in result
    assert 'task_id="task_a"' in result                                                                                                                                                                                                            
    assert 'bash_command="echo hello"' in result


def test_generate_dag_file():                                                                                                                                                                                                                      
    dag_config = {                                                                                                                                                                                                                                 
          "schedule": "@daily",                                                                                                                                                                                                                      
          "start_date": "2024-01-01",                                                                                                                                                                                                                
          "tasks": {                                        
              "task_a": {                                                                                                                                                                                                                            
                  "operator": "airflow.operators.bash.BashOperator",
                  "bash_command": "echo hello",
              }                                                                                                                                                                                                                                      
          }
    }                                                                                                                                                                                                                                              
    result = generate_dag_file("my_dag", dag_config)      
    assert "from airflow.operators.bash import BashOperator" in result
    assert 'dag_id="my_dag"' in result                                                                                                                                                                                                             
    assert "task_a = BashOperator(" in result
                                               