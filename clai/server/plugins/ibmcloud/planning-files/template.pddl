(define (problem deploy)
(:domain kube)
(:objects
username password tag name name-to-delete namespace host_port local_port cluster_name protocol yaml cluster-config - object
tcp nodeport - ptype
)

(:init
(= (total-cost) 0)
)

(:goal (and 
<GOAL>
))

(:metric minimize (total-cost)) 

)