(define (problem deploy)
(:domain kube)
(:objects
username password tag name name-to-delete namespace host_port local_port cluster_name protocol yaml cluster-config - object
tcp nodeport - ptype
)

(:init
(= (total-cost) 0)
(known username)
(known password)
(known name)
(known tag)
(known local_port)
)

(:goal (and 
(deployed)
))

(:metric minimize (total-cost)) 

)